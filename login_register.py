import streamlit as st
import sqlite3
from db import create_connection, create_login_table, authenticate_user_in_login, create_sign_up_table, insert_sign_up_data, authenticate_user_in_sign_up, insert_login_data
import datetime
import base64
from http.cookies import SimpleCookie

def login_register(conn):
    session_state = st.session_state
    session_state.authenticated = session_state.get('authenticated', False)
    session_state.registered = session_state.get('registered', True)
    session_state.option = session_state.get('option', "Login")

    # conn = create_connection('golveda.db')
    # if not conn:
    #         conn = create_connection('golveda.db')
    #         print(f"Connected to database: golveda.db")
    # else:
    #     print("Connection already established.")
    if conn is not None:
        # Check if the login table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logintable';")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            # Create the login table if it doesn't exist
            create_login_table(conn)
        else:
            print("Login table already exists.")
        create_sign_up_table(conn)

    option = session_state.option

    if option == "Login":
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
        st.button("Register", key="register_button", on_click=lambda: session_state.update(option="Register"))
        if login_button:
            if authenticate_user_in_login(conn, username, password):
                print('authenticated')
                session_state.authenticated = True
                session_state.username = username  # Store the username in the session state
                insert_login_data(conn, username, password)  # Insert login data with username and login time
                # conn.close()
                st.success("Login successful!")
                return session_state.authenticated  # Return True to indicate successful login
            else:
                st.error("Invalid username or password")
                return session_state.authenticated
        # if session_state.authenticated == True:
        # st.button("Register", key="register_button", on_click=lambda: session_state.update(option="Register"))

    elif option == "Register":
        with st.form("registration_form"):
            st.subheader("Register")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            register_button = st.form_submit_button("Register")
            # st.form_submit_button("Register", on_click=lambda: session_state.update(option="Login")if session_state.registered == True else st.error('Enter credentials first!'))
        st.button("Login", key="login_button", on_click=lambda: session_state.update(option="Login"))
        if register_button:
            if authenticate_user_in_sign_up(conn, username, email):
                print(f'{username}\n{email}\n {password}')
                insert_sign_up_data(conn, username, email, password)
                print('yess')
                session_state.registered = True
                st.success("Registration successful!")
                
            else:
                st.error("Username or email already exists.")
                return False  # Return False if neither login nor registration was successful
    # Apply CSS styles
    css = """
        <style>
            input.st-ae.st-bc.st-bd.st-be.st-bf.st-bg.st-bh.st-bi.st-bj.st-bk.st-bl.st-ah.st-bm.st-bn.st-bo.st-bp.st-bq.st-br.st-bs.st-bt.st-ax.st-ay.st-az.st-bu.st-b1.st-b2.st-bb.st-bv.st-bw.st-bx {
                color: black;
                caret-color: black; /* Change caret color to black */
            }
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)
if __name__ == "__main__":
    login_register()


