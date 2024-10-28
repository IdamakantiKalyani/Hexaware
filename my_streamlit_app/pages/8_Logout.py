import streamlit as st

# Check if the user is logged in by checking the session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login(username, password):
    # This function simulates a login process
    # Replace with your actual login validation logic
    if username == "user" and password == "pass":
        st.session_state['logged_in'] = True
    else:
        st.error("Invalid username or password")

def logout():
    # Clear the session state to log out the user
    st.session_state['logged_in'] = False
    st.success("You have been logged out.")

# Login form
if not st.session_state['logged_in']:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)

# Display the main app content and logout button if logged in
if st.session_state['logged_in']:
    st.subheader("Welcome to the Smart Recruiting Platform!")
    # Main content goes here

    # Logout button
    if st.button("Logout"):
        logout()
