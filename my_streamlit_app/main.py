import streamlit as st
import sqlite3
import hashlib

# Database setup
def create_db():
    conn = sqlite3.connect('recruitment.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    conn = sqlite3.connect('recruitment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def create_user(full_name, email, password, role):
    conn = sqlite3.connect('recruitment.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (full_name, email, password, role) VALUES (?, ?, ?, ?)',
                  (full_name, email, hash_password(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('recruitment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

# Initialize session state for login if not already initialized
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Streamlit App
create_db()

st.markdown("<h1 class='title'>🚀 Welcome to Smart Recruiting Platform!</h1>", unsafe_allow_html=True)

menu = ["Login", "Sign Up", "Password Recovery"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")
    email = st.text_input("Username or Email", placeholder="Enter your username or email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    remember_me = st.checkbox("Remember Me")
    
    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.success(f"Welcome {user[1]} ({user[4]})!")
            st.session_state.logged_in = True
            st.session_state.role = user[4]
            st.session_state.user_name = user[1]

            # Role-based redirection
            if user[4] == "Admin":
                st.write("Redirect to Admin Dashboard")
            elif user[4] == "HR Manager":
                st.write("Redirect to HR Manager Dashboard")
            elif user[4] == "Recruiter":
                st.write("Redirect to Recruiter Dashboard")
            elif user[4] == "Interviewer":
                st.write("Redirect to Interviewer Dashboard")
            elif user[4] == "Candidate":
                st.write("Redirect to Candidate Dashboard")
        else:
            st.error("Invalid username or password")
    
     

elif choice == "Sign Up":
    st.subheader("Sign Up")
    full_name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
    role = st.selectbox("Role", ["Admin", "HR Manager", "Recruiter", "Interviewer", "Candidate"])
    
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            if create_user(full_name, email, password, role):
                st.success("You have successfully signed up")
                st.info("Go to the Login page to log in")
            else:
                st.error("Email already exists. Please use a different email")

elif choice == "Password Recovery":
    st.subheader("Password Recovery")
    email = st.text_input("Email", placeholder="Enter your registered email")
    
    if st.button("Submit"):
        user = get_user_by_email(email)
        if user:
            st.success(f"A password recovery link has been sent to {email}")
            # This is where you would send an actual email with a password reset link
        else:
            st.error("Email not found")
