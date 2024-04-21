# import streamlit as st
# import sqlite3
# from db import create_connection, insert_sign_up_data, create_sign_up_table, authenticate_user_in_sign_up
# import login_page

# def register():
#     session_state = st.session_state
#     session_state.can_login = session_state.get('can_login', False)
#     conn = create_connection("golveda.db")
#     if conn is not None:
#         create_sign_up_table(conn)
#     else:
#         st.error("Error creating connection to database.")
#     if session_state.can_login == True:
#         conn.close
#         login_page.login()
#     else:
#         col1, col2, col3 = st.columns([1,3,1])
#         with col1:
#             pass
#         with col2:
#             username = st.text_input(label='Enter username')
#             email = st.text_input(label='Email')
#             password = st.text_input(label='Password', type = 'password')
#             sign_up_button = st.button('Sign up')
#             login_button = st.button("Login")
#             if sign_up_button:
#                 if authenticate_user_in_sign_up(conn, username, email):
#                     print(f'{username}\n{email}\n {password}')
#                     insert_sign_up_data(conn, username, email, password)
#                     session_state.can_login = True
#                     return session_state.can_login
#                     # st.success('Successfully signed up!')
#             elif login_button:
#                 # session_state.can_login = True
#                 session_state.can_login = True
#                 return session_state.can_login
#                 # st.experimental_rerun()
        
#         with col3:
#             pass

# if __name__ == "__main__":
#     register()
    

import streamlit as st
import sqlite3
from db import create_connection, insert_sign_up_data, create_sign_up_table, authenticate_user_in_sign_up

def register():
    session_state = st.session_state
    session_state.can_login = session_state.get('can_login', False)
    conn = create_connection("golveda.db")

    if conn is not None:
        create_sign_up_table(conn)
    else:
        st.error("Error creating connection to database.")

    with st.form("registration_form"):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            pass
        with col2:
            username = st.text_input(label='Enter username')
            email = st.text_input(label='Email')
            password = st.text_input(label='Password', type='password')
            sign_up_button = st.form_submit_button('Sign up')
        with col3:
            pass

        if sign_up_button:
            if authenticate_user_in_sign_up(conn, username, email):
                print(f'{username}\n{email}\n {password}')
                insert_sign_up_data(conn, username, email, password)
                session_state.can_login = True

    conn.close()

if __name__ == "__main__":
    register()