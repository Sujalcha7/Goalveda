import datetime
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
import streamlit as st
from db import authenticate_user_in_login, create_connection, create_login_table
from goalvedapp import main
# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create authenticator object
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def login():
    session_state = st.session_state

    if 'authenticated' not in session_state:
        session_state.authenticated = False

    conn = create_connection('golveda.db')
    create_login_table(conn)

    if session_state.authenticated:
        main()
    else:
        # Use st.tabs to create tabs for Login and Register
        # tabs = st.tabs(["Login", "Register"])

        # Initially, hide the Register tab
        # tabs[1].visible = False

        # Login tab content
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        if login_button:
            if authenticate_user_in_login(conn, username, password):
                # Set cookie expiration date
                expiration_date = datetime.datetime.now() + datetime.timedelta(days=config['cookie']['expiry_days'])
                st.set_cookie(config['cookie']['name'], 'true', expires=expiration_date)
                session_state.authenticated = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")


if __name__ == "__main__":
    login()