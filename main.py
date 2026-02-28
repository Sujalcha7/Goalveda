from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import bcrypt
from datetime import datetime

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "golveda.db"

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# --- Pydantic Models ---
class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    task_name: str
    username: str
    est_gol: int

class TaskUpdate(BaseModel):
    task_name: str
    new_task_name: str
    new_est_gol: int
    completed_pomodoros: int

class TaskUpdatePomodoros(BaseModel):
    task_name: str
    completed_pomodoros: int

# --- Auth Endpoints ---

@app.post("/api/signup")
def signup(user: UserSignUp, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_credentials WHERE username = ? OR email = ?", (user.username, user.email))
    existing_user = cursor.fetchone()
    
    if existing_user:
        if existing_user['username'] == user.username:
            raise HTTPException(status_code=400, detail="Username already taken")
        else:
            raise HTTPException(status_code=400, detail="Email already taken")
            
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute("INSERT INTO user_credentials (username, email, password) VALUES (?, ?, ?)", 
                       (user.username, user.email, hashed_password))
        db.commit()
        return {"message": "User registered successfully"}
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
def login(user: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT password FROM user_credentials WHERE username = ?", (user.username,))
    row = cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    hashed_password = row['password']
    
    # Handle legacy passwords (Streamlit implementation might have stored bytes directly or standard strings)
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
        
    if bcrypt.checkpw(user.password.encode('utf-8'), hashed_password):
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO logins (username, password, login_time) VALUES (?, ?, ?)", 
                       (user.username, "REDACTED", login_time))
        db.commit()
        return {"message": "Login successful", "username": user.username}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# --- Task Endpoints ---

@app.get("/api/tasks/{username}")
def get_tasks(username: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT task_name, est_gol, completed_pomodoros FROM tasks WHERE username = ?", (username,))
    tasks = cursor.fetchall()
    return [{"task_name": t['task_name'], "est_gol": t['est_gol'], "completed_pomodoros": t['completed_pomodoros']} for t in tasks]

@app.post("/api/tasks")
def create_task(task: TaskCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO tasks (username, task_name, est_gol, completed_pomodoros) VALUES (?, ?, ?, 0)",
                       (task.username, task.task_name, task.est_gol))
        db.commit()
        return {"message": "Task created successfully"}
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/tasks/{username}")
def update_task(username: str, task: TaskUpdate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET task_name = ?, est_gol = ?, completed_pomodoros = ? WHERE task_name = ? AND username = ?",
                   (task.new_task_name, task.new_est_gol, task.completed_pomodoros, task.task_name, username))
    db.commit()
    return {"message": "Task updated successfully"}

@app.patch("/api/tasks/{username}/pomodoros")
def update_pomodoros(username: str, task: TaskUpdatePomodoros, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET completed_pomodoros = ? WHERE task_name = ? AND username = ?",
                   (task.completed_pomodoros, task.task_name, username))
    db.commit()
    return {"message": "Pomodoros updated successfully"}

@app.delete("/api/tasks/{username}/{task_name}")
def delete_task(username: str, task_name: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_name = ? AND username = ?", (task_name, username))
    db.commit()
    return {"message": "Task deleted successfully"}

# Include startup event to initialize tables if they don't exist
@app.on_event("startup")
def startup_event():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_credentials (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL, 
                    email TEXT UNIQUE NOT NULL,
                    password varchar(200) NOT NULL
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    est_gol INTEGER NOT NULL,
                    completed_pomodoros INTEGER DEFAULT 0
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS logins (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    login_time TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()
