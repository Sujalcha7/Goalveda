# # goalveda_components.py

# import streamlit as st

# def add_navbar():
#    st.markdown(
#        """
#        <nav class="navbar">
#        <div class="navbar-brand">
#            <a href="#">Golveda</a>
#        </div>
#        <ul class="navbar-nav">
#            <li class="nav-item">
#            <a href="#" class="nav-link">Home</a>
#            </li>
#            <li class="nav-item">
#            <a href="#" class="nav-link">Tasks</a>
#            </li>
#            <li class="nav-item">
#            <a href="#" class="nav-link">Settings</a>
#            </li>
#            <li class="nav-item">
#             <a href="#" class="nav-link" onclick="showConfirmation()">Logout</a>
#             </li>
#        </ul>
#        <div class="navbar-toggle">
#            <span class="toggle-icon"></span>
#        </div>
#        </nav>
#        """,
#        unsafe_allow_html=True,
#    )

#    st.markdown(
#        """
#        <style>
#            /* Navbar styles */
#            .navbar {
#            display: flex;
#            justify-content: space-between;
#            align-items: center;
#            background-color: #AA4242;
#            color: #fff;
#            padding: 10px;
#            }

#            .navbar-brand a {
#            color: #fff;
#            text-decoration: none;
#            font-size: 24px;
#            font-weight: bold;
#            }

#            .navbar-nav {
#            display: flex;
#            list-style-type: none;
#            margin: 0;
#            padding: 0;
#            margin-left: auto; /* Align navbar-nav to the right */
#            }

#            .nav-item {
#            margin-right: 20px;
#            color: #000000
#            }
   
#            .nav-link {
#                color: #ffffff !important;/* Set the text color to white */
#                text-decoration: none;
#                padding: 8px 12px;
#                border-radius: 4px;
#                transition: background-color 0.3s ease;
#            }

#            .nav-link:hover {
#            background-color: #fff; /* Show button borders with white backgrounds on hover */
#            color: #000000 !important;
#            text-decoration: none;
#            }

#            /* Responsive styles */
#            @media (max-width: 768px) {
#            .navbar-nav {
#                display: none;
#                flex-direction: column;
#                position: absolute;
#                top: 60px;
#                left: 0;
#                width: 100%;
#                background-color: #333;
#                padding: 10px;
#            }

#            .nav-item {
#                margin: 10px 0;
#            }

#            .nav-link {
#                color: #fff;
#            }

#            .navbar-toggle {
#                display: block;
#                cursor: pointer;
#            }

#            .toggle-icon {
#                display: block;
#                width: 25px;
#                height: 3px;
#                background-color: #fff;
#                position: relative;
#            }

#            .toggle-icon::before,
#            .toggle-icon::after {
#                content: "";
#                display: block;
#                width: 25px;
#                height: 3px;
#                background-color: #fff;
#                position: absolute;
#                left: 0;
#            }

#            .toggle-icon::before {
#                top: -8px;
#            }

#            .toggle-icon::after {
#                bottom: -8px;
#            }
#        </style>
#        """,
#        unsafe_allow_html=True,
#    )

#    st.components.v1.html(
#        """
#        <script>
#             const navbarToggle = document.querySelector('.navbar-toggle');
#             const navbarNav = document.querySelector('.navbar-nav');

#             navbarToggle.addEventListener('click', () => {
#                 navbarNav.classList.toggle('active');
#             });
#             function showConfirmation() {
#                 if (confirm("Are you sure you want to log out?")) {
#                     window.parent.logout();
#                 }
#             }
#        </script>
#        """,
#        height=0,
#    )



import streamlit as st

import streamlit as st

def add_navbar():
    st.markdown(
        """
        <nav class="navbar">
        <div class="navbar-brand">
            <a href="#">Golveda</a>
        </div>
        <ul class="navbar-nav">
            <li class="nav-item">
            <a href="#" class="nav-link">Home</a>
            </li>
            <li class="nav-item">
            <a href="#" class="nav-link">Tasks</a>
            </li>
            <li class="nav-item">
            <a href="#" class="nav-link">Settings</a>
            </li>
            <li class="nav-item">
            <a href="#" class="nav-link" onclick="logoutClick()">Logout</a>
            </li>
        </ul>
        <div class="navbar-toggle">
            <span class="toggle-icon"></span>
        </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
            /* Navbar styles */
            .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #AA4242;
            color: #fff;
            padding: 10px;
            }

            .navbar-brand a {
            color: #fff;
            text-decoration: none;
            font-size: 24px;
            font-weight: bold;
            }

            .navbar-nav {
            display: flex;
            list-style-type: none;
            margin: 0;
            padding: 0;
            margin-left: auto; /* Align navbar-nav to the right */
            }

            .nav-item {
            margin-right: 20px;
            color: #000000
            }

            .nav-link {
                color: #ffffff !important;/* Set the text color to white */
                text-decoration: none;
                padding: 8px 12px;
                border-radius: 4px;
                transition: background-color 0.3s ease;
            }

            .nav-link:hover {
            background-color: #fff; /* Show button borders with white backgrounds on hover */
            color: #000000 !important;
            text-decoration: none;
            }

            /* Responsive styles */
            @media (max-width: 768px) {
            .navbar-nav {
                display: none;
                flex-direction: column;
                position: absolute;
                top: 60px;
                left: 0;
                width: 100%;
                background-color: #333;
                padding: 10px;
            }

            .nav-item {
                margin: 10px 0;
            }

            .nav-link {
                color: #fff;
            }

            .navbar-toggle {
                display: block;
                cursor: pointer;
            }

            .toggle-icon {
                display: block;
                width: 25px;
                height: 3px;
                background-color: #fff;
                position: relative;
            }

            .toggle-icon::before,
            .toggle-icon::after {
                content: "";
                display: block;
                width: 25px;
                height: 3px;
                background-color: #fff;
                position: absolute;
                left: 0;
            }

            .toggle-icon::before {
                top: -8px;
            }

            .toggle-icon::after {
                bottom: -8px;
            }
        </style>
        <script>
            const navbarToggle = document.querySelector('.navbar-toggle');
            const navbarNav = document.querySelector('.navbar-nav');

            navbarToggle.addEventListener('click', () => {
              navbarNav.classList.toggle('active');
            });

            function logoutClick() {
                Streamlit.setSessionState({logout: true});
            }
        </script>
        """,
        unsafe_allow_html=True,
    )