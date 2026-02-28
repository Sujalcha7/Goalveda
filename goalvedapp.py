import streamlit as st
import sqlite3
import time
from db import create_connection, insert_data, update_completed_pomodoros, create_table
from login_register import login_register
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(page_title="Goalveda", page_icon="🍅", layout="centered")

# Initialize Cookie Manager
cookies = EncryptedCookieManager(prefix="goalveda", password="super_secret_password")
if not cookies.ready():
    st.stop()

def inject_custom_css(mode):
    bg_color = "#ba4949"
    if mode == "short_break":
        bg_color = "#38858a"
    elif mode == "long_break":
        bg_color = "#397097"

    css = f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            transition: background-color 0.5s ease;
        }}
        .stApp header {{
            background-color: transparent;
        }}
        .timer-text {{
            font-size: 1000px;
            font-weight: bold;
            color: white;
            text-align: center;
            margin: 0;
            padding: 0;
            line-height: 1;
        }}
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: background-color 0.2s ease;
        }}
        .stButton > button:hover {{
            background-color: rgba(255, 255, 255, 0.3);
            color: white;
        }}
        .start-button button {{
            background-color: white !important;
            color: {bg_color} !important;
            font-size: 24px !important;
            padding: 1rem 3rem !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 0 rgba(0,0,0,0.1) !important;
            display: block;
            margin: 0 auto;
        }}
        .task-container {{
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
            border-left: 6px solid {bg_color};
        }}
        /* Hide sidebar completely if not needed */
        [data-testid="collapsedControl"] {{
            display: none;
        }}
        h1, h2, h3, p, span, div, label {{
            color: white ;
        }}
        .task-container span, .task-container div {{
             color: #555 !important;
        }}
        .task-container form p {{
             color: #555 !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def delete_task(conn, task_name, username):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_name = ? AND username = ?", (task_name, username))
    conn.commit()

def main():
    conn = create_connection("golveda.db")
    if conn is not None:
        create_table(conn)
    
    logout_happened = False
    if st.session_state.get('logout_pending'):
        logout_happened = True
        
        # Aggressively delete everything from session state to prevent ghost cache
        keys_to_delete = list(st.session_state.keys())
        for key in keys_to_delete:
            del st.session_state[key]
            
        # Empty out the cookie
        if "username" in cookies:
            cookies["username"] = ""
            cookies.save()

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.timer_mode = 'pomodoro' # pomodoro, short_break, long_break
        st.session_state.timer_running = False
        st.session_state.time_left = 25 * 60
        st.session_state.settings = {'pomodoro': 25, 'short_break': 5, 'long_break': 15}
        st.session_state.active_task_name = None

    inject_custom_css(st.session_state.timer_mode)

    # Check Cookie Auth First
    if cookies.get("username") and not logout_happened:
        st.session_state.authenticated = True
        st.session_state.username = cookies.get("username")

    if not st.session_state.authenticated:
        if login_register(conn) == True:
            st.session_state.authenticated = True
            cookies["username"] = st.session_state.username # Save auth to cookie
            cookies.save()
            st.rerun()
        return

    # Top Navigation / Header
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("### 🍅 Goalveda")
    with col2:
        with st.expander("⚙️ Settings"):
            pomo_t = st.number_input("Pomodoro (min)", min_value=1, value=st.session_state.settings['pomodoro'])
            short_t = st.number_input("Short Break (min)", min_value=1, value=st.session_state.settings['short_break'])
            long_t = st.number_input("Long Break (min)", min_value=1, value=st.session_state.settings['long_break'])
            if st.button("Save Settings"):
                st.session_state.settings['pomodoro'] = pomo_t
                st.session_state.settings['short_break'] = short_t
                st.session_state.settings['long_break'] = long_t
                st.session_state.time_left = st.session_state.settings[st.session_state.timer_mode] * 60
                st.rerun()
    with col3:
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False 
            st.session_state.logout_pending = True
            st.rerun()

    # --- TIMER COMPONENT ---
    st.write("---")
    t_col1, t_col2, t_col3 = st.columns([1, 1, 1])
    with t_col1:
        if st.button("Pomodoro", use_container_width=True):
            st.session_state.timer_mode = 'pomodoro'
            st.session_state.timer_running = False
            st.session_state.time_left = st.session_state.settings['pomodoro'] * 60
            st.rerun()
    with t_col2:
        if st.button("Short Break", use_container_width=True):
            st.session_state.timer_mode = 'short_break'
            st.session_state.timer_running = False
            st.session_state.time_left = st.session_state.settings['short_break'] * 60
            st.rerun()
    with t_col3:
        if st.button("Long Break", use_container_width=True):
            st.session_state.timer_mode = 'long_break'
            st.session_state.timer_running = False
            st.session_state.time_left = st.session_state.settings['long_break'] * 60
            st.rerun()

    timer_placeholder = st.empty()
    
    # We use a container specifically for the button to style it correctly via CSS
    st.markdown('<div class="start-button">', unsafe_allow_html=True)
    if st.session_state.timer_running:
        if st.button("PAUSE", use_container_width=True):
            st.session_state.timer_running = False
            st.rerun()
    else:
        if st.button("START", use_container_width=True):
            st.session_state.timer_running = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Display initial time
    mins, secs = divmod(st.session_state.time_left, 60)
    timer_placeholder.markdown(f'<div style="text-align: center; font-size: 10rem; font-weight: bold; color: white; line-height: 1;">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # --- TASKS COMPONENT ---
    st.write("---")
    st.subheader("Tasks")
    
    # Add Task Form
    with st.expander("➕ Add Task"):
        new_task = st.text_input("What are you working on?")
        est_pomodoros = st.number_input("Est Pomodoros", min_value=1, step=1, value=1)
        if st.button("Save Task"):
            if new_task:
                username = st.session_state.get('username', 'user')
                insert_data(conn, username, new_task, est_pomodoros)
                st.success("Task added!")
                st.rerun()

    # List Tasks
    cursor = conn.cursor()
    username = st.session_state.get('username', 'user')
    cursor.execute("SELECT task_name, est_gol, completed_pomodoros FROM tasks WHERE username = ?", (username,))
    tasks = cursor.fetchall()
    
    if not tasks:
        st.info("No tasks yet. Add one above!")
    else:
        for task in tasks:
            t_name, est_gol, completed = task
            is_active = (st.session_state.get('active_task_name') == t_name)
            
            with st.container():
                st.markdown(f'''
                    <div class="task-container" style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-size:1.1rem; color: #555 !important;">{t_name}</div>
                        <div style="font-size:1.1rem; color: #555 !important; font-weight: bold;">{completed} / {est_gol}</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1,1,2])
                with c1:
                    if is_active:
                        st.button("🎯 Active", key=f"active_{t_name}", disabled=True)
                    else:
                        if st.button("Set Active", key=f"set_active_{t_name}"):
                            st.session_state.active_task_name = t_name
                            st.rerun()
                with c2:
                    if st.button("🗑️ Delete", key=f"del_{t_name}"):
                        delete_task(conn, t_name, username)
                        if st.session_state.get('active_task_name') == t_name:
                            st.session_state.active_task_name = None
                        st.rerun()

    # Timer Loop execution (must run last to allow rendering above it)
    if st.session_state.timer_running:
        while st.session_state.time_left > 0 and st.session_state.timer_running:
            time.sleep(1)
            st.session_state.time_left -= 1
            mins, secs = divmod(st.session_state.time_left, 60)
            timer_placeholder.markdown(f'<div style="text-align: center; font-size: 15rem; font-weight: bold; color: white; line-height: 1;">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
            
        if st.session_state.time_left == 0:
            st.session_state.timer_running = False
            
            # Automatically update the completed pomodoros if it's a pomodoro session
            if st.session_state.timer_mode == 'pomodoro' and st.session_state.get('active_task_name'):
                cursor = conn.cursor()
                cursor.execute("SELECT completed_pomodoros FROM tasks WHERE task_name = ? AND username = ?", (st.session_state.active_task_name, username))
                row = cursor.fetchone()
                if row:
                    update_completed_pomodoros(conn, st.session_state.active_task_name, username, row[0] + 1)
                    
            # Play an alert via HTML audio tag
            autoplay_audio = '''
                <audio autoplay="true">
                <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                </audio>
            '''
            st.markdown(autoplay_audio, unsafe_allow_html=True)
            st.success("Time's up!")
            st.session_state.time_left = st.session_state.settings[st.session_state.timer_mode] * 60
            time.sleep(2) # Give user a chance to hear audio
            st.rerun()

if __name__ == "__main__":
    main()
