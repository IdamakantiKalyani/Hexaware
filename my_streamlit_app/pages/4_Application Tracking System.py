import os
import streamlit as st
import sqlite3
from datetime import datetime
st.title("Application Tracking System")
# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access the Application Tracking System.")
    st.stop()

# Database setup
def create_connection():
    conn = sqlite3.connect('job_categories.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Create Jobs table
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        department TEXT,
                        location TEXT)''')

    # Create Applications table
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY,
                        applicant_name TEXT NOT NULL,
                        email TEXT,
                        phone TEXT,
                        resume_path TEXT,
                        job_id INTEGER,
                        status TEXT,
                        date_applied DATE,
                        FOREIGN KEY (job_id) REFERENCES jobs (id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY,
                        message TEXT,
                        date DATE,
                        is_read BOOLEAN)''')
    conn.commit()
    conn.close()

create_tables()

# Option 1: Add resume_path column if it doesn't exist
def add_resume_path_column():
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the resume_path column exists
    cursor.execute("PRAGMA table_info(applications)")
    columns = cursor.fetchall()

    if 'resume_path' not in [column[1] for column in columns]:
        cursor.execute("ALTER TABLE applications ADD COLUMN resume_path TEXT")
        conn.commit()

    conn.close()

add_resume_path_column()

# Ensure 'resumes/' directory exists
def ensure_resume_directory():
    if not os.path.exists("resumes"):
        os.makedirs("resumes")

# Application Submission Screen
def application_submission():
    st.title("Job Application Submission")
    conn = create_connection()
    cursor = conn.cursor()

    # Ensure resume directory exists
    ensure_resume_directory()

    # Job Titles Dropdown
    cursor.execute("SELECT title FROM jobs")
    job_titles = [job[0] for job in cursor.fetchall()]

    if not job_titles:
        st.warning("No job postings available.")
        return

    selected_job_title = st.selectbox("Select Job Title", job_titles)

    # Applicant Details
    applicant_name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    # Resume Upload (Limit 20MB)
    resume = st.file_uploader("Upload Resume (PDF, Max: 20MB)", type=["pdf"])
    if resume and resume.size > 20 * 1024 * 1024:  # 20MB limit
        st.error("File size exceeds 20MB. Please upload a smaller file.")
        return

    if st.button("Submit Application"):
        if not applicant_name or not email or not phone or not resume:
            st.error("Please fill out all fields and upload your resume.")
        else:
            # Save resume to disk
            resume_path = f"resumes/{email}_{resume.name}"
            with open(resume_path, "wb") as f:
                f.write(resume.read())

            # Insert application into database
            cursor.execute("SELECT id FROM jobs WHERE title=?", (selected_job_title,))
            job_id = cursor.fetchone()[0]
            cursor.execute('''INSERT INTO applications (applicant_name, email, phone, resume_path, job_id, status, date_applied)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (applicant_name, email, phone, resume_path, job_id, 'Applied', datetime.now()))
            conn.commit()

            st.success(f"Application submitted successfully for {selected_job_title}!")

# Application Tracking Screen
def track_application():
    st.title("Track Your Application")
    email = st.text_input("Enter your email to track your application")

    if st.button("Track Application"):
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM applications WHERE email=?", (email,))
        app = cursor.fetchone()

        if app:
            st.subheader("Application Details")
            st.write(f"**Name:** {app[1]}")
            st.write(f"**Email:** {app[2]}")
            st.write(f"**Phone:** {app[3]}")
            st.write(f"**Resume:** [Download]({app[4]})")
            cursor.execute("SELECT title FROM jobs WHERE id=?", (app[5],))
            job_title = cursor.fetchone()[0]
            st.write(f"**Job Title:** {job_title}")
            st.write(f"**Application Status:** {app[6]}")
            st.write(f"**Date Applied:** {app[7]}")
        else:
            st.error("No applications found for the given email.")

# Main application
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Submit Application", "Track Application"])

    if page == "Submit Application":
        application_submission()
    elif page == "Track Application":
        track_application()

if __name__ == "__main__":
    main()
