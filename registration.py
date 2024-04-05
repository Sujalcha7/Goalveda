import streamlit as st
import sqlite3
from db import create_connection, insert_sign_up_data, create_sign_up_table, authenticate_user_in_sign_up


def register():
    conn = create_connection("golveda.db")
    if conn is not None:
        create_sign_up_table(conn)
    else:
        st.error("Error creating connection to database.")
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        pass
    with col2:
        username = st.text_input(label='Enter username')
        email = st.text_input(label='Email')
        password = st.text_input(label='Password', type = 'password')
        sign_up_button = st.button('Sign up')
        if sign_up_button:
            if authenticate_user_in_sign_up(conn, username, email):
                print(f'{username}\n{email}\n {password}')
                insert_sign_up_data(conn, username, email, password)
                print('Successfully signed up!')
        
    with col3:
        pass

if __name__ == "__main__":
    register()
    