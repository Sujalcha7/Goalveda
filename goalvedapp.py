import streamlit as st
import sqlite3
from db import *
from login_register import login_register
import pandas as pd

def main():
    session_state = st.session_state
    conn = create_connection("golveda.db")
    session_state.authenticated = session_state.get('authenticated', False)
    session_state.page = session_state.get('page', 'login_register')

    if conn is not None:
        create_table(conn)  # Create the table with the updated schema
    else:
        st.error("Error creating connection to database.")

    page = session_state.page
    if page == 'login_register':
        if login_register() == True:
            session_state.authenticated = True
        if session_state.authenticated == True:
            session_state.update(page='main_page')
            st.experimental_rerun()  # Add this line
    elif page == 'main_page':
        # Insert data form
        buff, col, buff2 = st.columns([1, 3, 1])
        with col:
            st.subheader("Insert Data")
            name = st.text_input('New task:')
            age = st.text_input('est. pomodoros:')
            if st.button("Insert"):
                if name and age:
                    username = session_state.get('username', '')  # Retrieve the username from the session state
                    insert_data(conn, username, name, age)
                else:
                    st.warning("Please fill in both name and age.")

        # Display tasks table
        buff, col, buff2 = st.columns([1, 3, 1])
        with col:
            st.subheader("Tasks")
            cursor = conn.cursor()
            username = session_state.get('username')  # Retrieve the username from the session state
            cursor.execute('''SELECT task_name, est_gol FROM tasks WHERE username = ?''', (username,))
            tasks = cursor.fetchall()
            if tasks:
                tasks_df = pd.DataFrame(tasks, columns=['task name', 'est. pomo'])
                st.table(tasks_df)
            else:
                st.info("No tasks added yet.")

    conn.close()

if __name__ == "__main__":
    main()