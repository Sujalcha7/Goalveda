import streamlit as st
import sqlite3
from db import *
from login_register import login_register
import pandas as pd
import timer

def delete_task(conn, task_name, username):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_name = ? AND username = ?", (task_name, username))
    conn.commit()

def update_task(conn, old_task_name, new_task_name, new_est_gol, username):
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task_name = ?, est_gol = ? WHERE task_name = ? AND username = ?", (new_task_name, new_est_gol, old_task_name, username))
    conn.commit()

def main():
    session_state = st.session_state
    conn = create_connection("golveda.db")
    session_state.authenticated = session_state.get('authenticated', False)
    session_state.page = session_state.get('page', 'login_register')
    session_state.timer_duration = session_state.get('timer_duration', 25)
    page = session_state.page

    if 'edit_task_name' not in session_state:
        session_state.edit_task_name = None

    # Show the login/register page without sidebar
    if not session_state.authenticated:
        if login_register(conn) == True:
            session_state.authenticated = True
        if session_state.authenticated == True:
            session_state.update(page='Homepage')  # Redirect to Homepage after successful login
            st.experimental_rerun()
    else:
        # Render the sidebar
        with st.sidebar:
            st.header("Navigation")
            page = session_state.page
            homepage_button = st.button("Homepage", key="homepage_button", on_click=lambda: session_state.update(page="Homepage"))
            tasks_button = st.button("Tasks", key="tasks_button", on_click=lambda: session_state.update(page="Tasks"))
            settings_button = st.button("Settings", key="settings_button", on_click=lambda: session_state.update(page="Settings"))
            logout_button = st.button("Logout", key="logout_button", on_click=lambda: session_state.update(page="Logout"))

        if page == 'Homepage':
            st.title("Welcome to Goalveda!")
            # Add any other content for the homepage here

        elif page == 'Tasks':
            display_tasks(conn, session_state)

        elif page == 'Settings':
            timer_duration = st.number_input("Set Timer Duration (minutes)", min_value=1, value=session_state.timer_duration)
            session_state.timer_duration = timer_duration

        elif page == 'Logout':
            # Clear session state and redirect to login page
            for key in st.session_state.keys():
                del st.session_state[key]
            session_state.update(page='login_register')
            st.experimental_rerun()

    # Apply CSS styles
    css = """
        <style>
            .stButton button {
                width: 120px;
                height: 40px;
                font-size: 16px;
                transition: background-color 0.3s, color 0.3s;
            }
            .stButton button:hover {
                background-color: white;
                color: black;
            }
            .st-emotion-cache-cnbvxy.e1nzilvr5 h1 {
                font-size: 80px;
                text-align: center
            }
            input.st-ae.st-bc.st-bd.st-be.st-bf.st-bg.st-bh.st-bi.st-bj.st-bk.st-bl.st-ah.st-bm.st-bn.st-bo.st-bp.st-bq.st-br.st-bs.st-bt.st-ax.st-ay.st-az.st-bu.st-b1.st-b2.st-bb.st-bv.st-bw.st-bx {
                color: black;
                caret-color: black; /* Change caret color to black */
            }
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)
def display_tasks(conn, session_state):
    buff, col, buff2 = st.columns([1, 3, 1])
    with col:
        session_state.stopped = timer.main(session_state.timer_duration)

        st.subheader("Insert Data")
        name = st.text_input('New task:')
        est_gol = st.number_input('est. pomodoros:', step=5, min_value=1, max_value=60)
        if st.button("Insert"):
            if name and est_gol:
                username = session_state.get('username', '')
                insert_data(conn, username, name, est_gol)
            else:
                st.warning("Please fill in both name and est_gol.")

    # Display tasks
    buff, col1, col2 = st.columns([1, 3, 1])
    with col1:
        st.subheader("Tasks")
        cursor = conn.cursor()
        username = session_state.get('username')
        cursor.execute('''SELECT task_name, est_gol, completed_pomodoros FROM tasks WHERE username = ?''', (username,))
        tasks = cursor.fetchall()
        if tasks:
            checked_tasks = []
            for task in tasks:
                task_name, est_gol, completed_pomodoros = task
                # print(task)
                # print(est_gol)
                # print(completed_pomodoros)
                exceeded_est = int(completed_pomodoros) > int(est_gol)
                checkbox_label = f"{task_name} - {completed_pomodoros}/{est_gol} pomodoros"
                if exceeded_est:
                    st.success('Exceeded Estimated Pomodoros! to further continuem, Edit the task')
                    checkbox_label += " (Exceeded Estimated Pomodoros)"
                checked = st.checkbox(checkbox_label, key=task_name)
                if checked:
                    session_state.edit_task_name = task_name
                    checked_tasks.append(task_name)
                    if session_state.get('timer_completed', True) or session_state.get('stopped', True):
                        # if completed_pomodoros < est_gol and session_state.edit_task_name == task_name:
                        if completed_pomodoros < est_gol:
                            print("incrementing", task)
                            update_completed_pomodoros(conn, task_name, username, completed_pomodoros + 1)
                        session_state.timer_completed = False
                        session_state.stopped = False
                    # else:
                    #     if session_state.edit_task_name != task_name:
                    #         session_state.edit_task_name = None

            buff, col1, col2, buff2 = st.columns([1, 2, 2, 1])
            with col1:
                submit_delete = st.button("Delete Tasks")
                if submit_delete:
                    for task_name in checked_tasks:
                        delete_task(conn, task_name, username)
                        session_state.edit_task_name =  None
                    st.experimental_rerun()

            with col2:
                edit_task_button = st.button("Edit Task")
                session_state.edit_button=edit_task_button;

                # if session_state.edit_button:
                if True:
                    if checked_tasks and len(checked_tasks) == 1:
                        session_state.edit_task_name = checked_tasks[0]
                    if session_state.edit_task_name:
                        # print('edit')
                        new_task_name = st.text_input("New Task Name", value=session_state.edit_task_name)
                        task_to_edit = session_state.edit_task_name
                        cursor.execute("SELECT est_gol, completed_pomodoros FROM tasks WHERE task_name = ? AND username = ?", (task_to_edit, username))
                        current_est_gol, current_completed_pomodoros = cursor.fetchone()
                        new_est_gol = st.text_input("New Estimated Pomodoros", value=current_est_gol)
                        submit_edit = st.button("Update Task")
                        session_state.update_button = submit_edit;
                        print("edit fetch", session_state.edit_task_name, new_task_name)

                        if session_state.update_button:
                            print("hello")
                            update_task(conn=conn, old_task_name=session_state.edit_task_name, new_task_name=new_task_name, new_est_gol=new_est_gol, username=username)
                            session_state.edit_task_name = None
                            st.experimental_rerun()
        else:
            st.info("No tasks added yet.")

    # Update the timer_completed flag when the timer is stopped or completed
    if session_state.get('stopped', False) or (session_state.get('remaining_time', 0)==0):
        session_state.timer_completed = True
        session_state.stopped = False
if __name__ == "__main__":
    main()

