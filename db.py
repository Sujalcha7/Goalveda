import sqlite3
import streamlit as st
import bcrypt
from datetime import datetime
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to SQLite database: {e}")
    return conn

# Function to create table in SQLite database
def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        task_name TEXT NOT NULL,
                        username TEXT NOT NULL,
                        est_gol INTEGER NOT NULL
                     )''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error creating table: {e}")

# Function to insert data into SQLite database
def insert_data(conn, username, task_name, est):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO tasks (username, task_name, est_gol) VALUES (?, ?, ?)''', (username, task_name, est))
        conn.commit()
        st.success("Data inserted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error inserting data: {e}")


def create_login_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logins (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        login_time TEXT NOT NULL
                     )''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error creating table: {e}")

# Function to insert data into SQLite database
def insert_login_data(conn, username, password):
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO logins (username, password, login_time) VALUES (?, ?, ?)''', (username, password, login_time))
        conn.commit()
        st.success("Login successful!")
    except sqlite3.Error as e:
        st.error(f"Error inserting data: {e}")


def create_sign_up_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_credentials (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL, 
                        email TEXT NOT NULL,
                        password varchar(20) NOT NULL
                     )''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error creating table: {e}")

def insert_sign_up_data(conn, username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(hashed_password)
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO user_credentials (username, email, password) VALUES (?, ?, ?)''', (username, email, hashed_password))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.commit()
        print("Data inserted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error inserting data: {e}")

def authenticate_user_in_login(conn, username, password):
    authenticated = False
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT password FROM user_credentials WHERE username = ?''', (username, ))
        hashed_password = cursor.fetchone()
        print(hashed_password)
        if hashed_password:
            # Verify password using bcrypt.checkpw
            authenticated = bcrypt.checkpw(password.encode('utf-8'), hashed_password[0])
            print(authenticated)
            if authenticated:
                return True
        else:
            print('invalid login!')
            st.write('Invalid Username or Password!')
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    return False

def authenticate_user_in_sign_up(conn, username, email):
    authenticated = False
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM user_credentials WHERE username = ? or email = ?''', (username, email))
            user = cursor.fetchone()
            if user:
                # If a user is found, check if it's due to username or email collision
                if user[1] == username:
                    st.write('Username already taken!')
                else:
                    st.write('Email already taken!')
            else:
                authenticated = True
            return authenticated
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
