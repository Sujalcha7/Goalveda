# import streamlit as st
# import sqlite3
# from db import *
# from login_register import login_register
# import pandas as pd
# from nav_bar import add_navbar
# import timer 
# from logout_componentn import load_logout_component

# def delete_task(conn, task_name, username):
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM tasks WHERE task_name = ? AND username = ?", (task_name, username))
#     conn.commit()

# def update_task(conn, old_task_name, new_task_name, new_est_gol, username):
#     cursor = conn.cursor()
#     cursor.execute("UPDATE tasks SET task_name = ?, est_gol = ? WHERE task_name = ? AND username = ?", (new_task_name, new_est_gol, old_task_name, username))
#     conn.commit()

# # def logout():
# #     # Clear session state
# #     for key in st.session_state.keys():
# #         del st.session_state[key]

# #     # Redirect to the login page
# #     st.session_state.page = 'login_register'
# #     st.experimental_rerun()

# def main():
#     session_state = st.session_state
#     conn = create_connection("golveda.db")
#     session_state.authenticated = session_state.get('authenticated', False)
#     session_state.page = session_state.get('page', 'login_register')
#     page = session_state.page

#     if 'edit_task_name' not in session_state:
#         session_state.edit_task_name = None

#     if not session_state.authenticated:
#         session_state.update(page='login_register')

#     if page == 'login_register':
#         if login_register(conn) == True:
#             session_state.authenticated = True
#         if session_state.authenticated == True:
#             session_state.update(page='main_page')
#             st.experimental_rerun()

#     elif page == 'main_page':
        
#         # Insert data form
#         buff, col, buff2 = st.columns([1, 3, 1])
#         with col:
#             timer.main()

#             st.subheader("Insert Data")
#             name = st.text_input('New task:')
#             age = st.text_input('est. pomodoros:')
#             if st.button("Insert"):
#                 if name and age:
#                     username = session_state.get('username', '')
#                     insert_data(conn, username, name, age)
#                 else:
#                     st.warning("Please fill in both name and age.")

#         # Display tasks
#         buff, col1, col2 = st.columns([1, 3, 1])
#         with col1:
#             st.subheader("Tasks")
#             cursor = conn.cursor()
#             username = session_state.get('username')
#             cursor.execute('''SELECT task_name, est_gol FROM tasks WHERE username = ?''', (username,))
#             tasks = cursor.fetchall()
#             if tasks:
#                 checked_tasks = []
#                 for task in tasks:
#                     task_name, est_gol = task
#                     checked = st.checkbox(f"{task_name} - {est_gol} pomodoros", key=task_name)
#                     if checked:
#                         checked_tasks.append(task_name)
#                     else:
#                         if session_state.edit_task_name == task_name:
#                             session_state.edit_task_name = None

#                 # if checked_tasks:
#                 buff,col1, col2,buff2 = st.columns([1,2,2,1])
#                 with col1:
#                     submit_delete = st.button("Delete Tasks")
#                     if submit_delete:
#                         for task_name in checked_tasks:
#                             delete_task(conn, task_name, username)
#                         st.experimental_rerun()

#                 with col2:
#                     edit_task_button = st.button("Edit Task")
#                     if edit_task_button:
#                         if checked_tasks:
#                             session_state.edit_task_name = checked_tasks[0]
#                     if session_state.edit_task_name:
#                         new_task_name = st.text_input("New Task Name", value=session_state.edit_task_name)
#                         task_to_edit = session_state.edit_task_name
#                         cursor.execute("SELECT est_gol FROM tasks WHERE task_name = ? AND username = ?", (task_to_edit, username))
#                         current_est_gol = cursor.fetchone()[0]
#                         new_est_gol = st.text_input("New Estimated Pomodoros", value=current_est_gol)
#                         submit_edit = st.button("Update Task")
#                         if submit_edit:
#                             update_task(conn, session_state.edit_task_name, new_task_name, new_est_gol, username)
#                             session_state.edit_task_name = None
#                             st.experimental_rerun()
#             else:
#                 st.info("No tasks added yet.")

#     # Apply CSS styles
#     css = """
#         <style>
#             .stButton button {
#                 width: 120px;
#                 height: 40px;
#                 font-size: 16px;
#             }
#             input.st-ae.st-bc.st-bd.st-be.st-bf.st-bg.st-bh.st-bi.st-bj.st-bk.st-bl.st-ah.st-bm.st-bn.st-bo.st-bp.st-bq.st-br.st-bs.st-bt.st-ax.st-ay.st-az.st-bu.st-b1.st-b2.st-bb.st-bv.st-bw.st-bx {

#                 color: black;

#                 caret-color: black; /* Change caret color to black */

#             }
#         </style>
#     """
#     st.markdown(css, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()



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
        timer.main(session_state.timer_duration)

        st.subheader("Insert Data")
        name = st.text_input('New task:')
        age = st.text_input('est. pomodoros:')
        if st.button("Insert"):
            if name and age:
                username = session_state.get('username', '')
                insert_data(conn, username, name, age)
            else:
                st.warning("Please fill in both name and age.")

    # Display tasks
    buff, col1, col2 = st.columns([1, 3, 1])
    with col1:
        st.subheader("Tasks")
        cursor = conn.cursor()
        username = session_state.get('username')
        cursor.execute('''SELECT task_name, est_gol FROM tasks WHERE username = ?''', (username,))
        tasks = cursor.fetchall()
        if tasks:
            checked_tasks = []
            for task in tasks:
                task_name, est_gol = task
                checked = st.checkbox(f"{task_name} - {est_gol} pomodoros", key=task_name)
                if checked:
                    checked_tasks.append(task_name)
                else:
                    if session_state.edit_task_name == task_name:
                        session_state.edit_task_name = None

            buff, col1, col2, buff2 = st.columns([1, 2, 2, 1])
            with col1:
                submit_delete = st.button("Delete Tasks")
                if submit_delete:
                    for task_name in checked_tasks:
                        delete_task(conn, task_name, username)
                    st.experimental_rerun()

            with col2:
                edit_task_button = st.button("Edit Task")
                if edit_task_button:
                    if checked_tasks:
                        session_state.edit_task_name = checked_tasks[0]
                if session_state.edit_task_name:
                    new_task_name = st.text_input("New Task Name", value=session_state.edit_task_name)
                    task_to_edit = session_state.edit_task_name
                    cursor.execute("SELECT est_gol FROM tasks WHERE task_name = ? AND username = ?", (task_to_edit, username))
                    current_est_gol = cursor.fetchone()[0]
                    new_est_gol = st.text_input("New Estimated Pomodoros", value=current_est_gol)
                    submit_edit = st.button("Update Task")
                    if submit_edit:
                        update_task(conn, session_state.edit_task_name, new_task_name, new_est_gol, username)
                        session_state.edit_task_name = None
                        st.experimental_rerun()
        else:
            st.info("No tasks added yet.")

if __name__ == "__main__":
    main()