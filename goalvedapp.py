import streamlit as st
import sqlite3
from streamlit_option_menu  import option_menu
from db import *
# Function to establish connection to SQLite database




def option_menu():
    selected = option_menu(
        menu_title=None,
        options=['Golveda', 'reports', 'settings', 'login'],
        default_index=0,
        orientation='horizontal',
        styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},
        }
    )
    if selected == 'Golveda':
        st.title(f'You selected {selected}')
    if selected == 'reports':
        st.title(f'You selected {selected}')
    if selected == 'settings':
        st.title(f'You selected {selected}')
    if selected == 'login':
        st.title(f'You selected {selected}')

# Main function
def main_page():
    # Title and introduction
    # option_menu()
    # Connect to SQLite database
    conn = create_connection("golveda.db")

    # Create table if it doesn't exist
    if conn is not None:
        create_table(conn)
    else:
        st.error("Error creating connection to database.")

    # Insert data form
    st.subheader("Insert Data")
    buff, col, buff2 = st.columns([1,3,1])
    name = col.text_input('New task:')
    age = col.text_input('est. pomodoros:')
    if st.button("Insert"):
        if name and age:
            insert_data(conn, name, age)
        else:
            st.warning("Please fill in both name and age.")

# Entry point
if __name__ == "__main__":
    main_page()
