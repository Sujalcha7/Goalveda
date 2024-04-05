import pickle
from pathlib import Path
import streamlit as st
# import sqlite3
# import streamlit_authenticator as stauth
from db import create_connection, create_login_table, authenticate_user_in_login
from goalvedapp import main_page
from datetime import datetime, timedelta
import time






# def set_cookie_expiration(days):
#     exp_date = datetime.now() + timedelta(days=days)
#     exp_date_str = exp_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
#     st.write(f'<meta http-equiv="set-cookie" content="__exp={exp_date_str}; Path=/"> ', unsafe_allow_html=True)  # Set cookie expiration
# def get_user_credentials(conn, username):
#     try:
#         cursor = conn.cursor()
#         cursor.execute('''SELECT username, password FROM user_credentials WHERE username = ?''', (username,))
#         user_credentials = cursor.fetchone()
#         if user_credentials:
#             return user_credentials
#         else:
#             return None  # Username not found
#     except sqlite3.Error as e:
#         print(f"Error accessing table: {e}")

# def fetch_cookie_expiry_days(conn, username):
#     cursor = conn.cursor()
#     cursor.execute("SELECT cookie_expiry_days FROM user_credentials WHERE username = ?", (username,))
#     expiry_days = cursor.fetchone()
#     return expiry_days[0] if expiry_days else None  # Return the first element of the tuple (expiry_days)

# Set up cookie manager
cookie_manager = stx.CookieManager()

# Define a function to set cookie with expiry in days
def set_cookie_with_expiry_days(name, value, days):
  # Get cookie manager instance
  cookie_manager = BetterCookieManager()
  # Set cookie with expiry in days
  cookie_manager.set(name, value, expires=days * 24 * 60 * 60)

# Example usage: Set cookie with 7-day expiry
set_cookie_with_expiry_days("user_id", "123", 7)

# Check if cookie exists
if "user_id" in cookie_manager.get_all():
  st.write("Welcome back!")
else:
  st.write("Please log in to continue.")


def login():
    session_state = st.session_state
    
    if 'authenticated' not in session_state:
        session_state.authenticated = False

    conn = create_connection('golveda.db')
    create_login_table(conn)

    if session_state.authenticated:
        main_page()
    else:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        if login_button:
            if authenticate_user_in_login(conn, username, password):
                session_state.authenticated = True
                set_cookie_with_expiry_days("user_id", "123", 7) 
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")


if __name__ == "__main__":
    login()
