# Goalveda

A Pomodoro-style task tracker built with Streamlit + SQLite.

## Run (Windows)

### 1) Create & activate a virtual environment (recommended)

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 2) Install dependencies

```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

### 3) Start the app

From the project folder:

```powershell
streamlit run goalvedapp.py
```

Or (most reliable) run Streamlit via the project's virtual environment:

```powershell
.\.venv\Scripts\python.exe -m streamlit run goalvedapp.py
```

Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser.

## Notes

- The app uses `golveda.db` (SQLite) in the project directory.
- First run will create the needed tables automatically.
