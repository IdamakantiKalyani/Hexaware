import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize schedule storage
if "schedule" not in st.session_state:
    st.session_state["schedule"] = []

st.title("Interview Scheduling")

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access the Interview Scheduling page.")
    st.stop()

# Input fields for scheduling
st.header("Schedule an Interview")
with st.form("interview_form"):
    candidate_name = st.text_input("Candidate Name")
    candidate_email = st.text_input("Candidate Email")
    interview_date = st.date_input("Interview Date", min_value=datetime.today().date())
    interview_time = st.time_input("Interview Time", value=datetime.now().time())
    interview_duration = st.number_input("Interview Duration (minutes)", min_value=15, max_value=180, value=30)
    
    # Interview mode selection
    interview_mode = st.selectbox("Interview Mode", ["In-person", "Video Call", "Phone Call"])
    
    # Show location only if mode is "In-person"
    interview_location = ""
    if interview_mode == "In-person":
        interview_location = st.text_input("Interview Location")

    submit = st.form_submit_button("Schedule Interview")

# Handling the form submission
if submit:
    end_time = (datetime.combine(interview_date, interview_time) + timedelta(minutes=interview_duration)).time()
    interview_details = {
        "Candidate Name": candidate_name,
        "Email": candidate_email,
        "Date": interview_date,
        "Start Time": interview_time,
        "End Time": end_time,
        "Mode": interview_mode,
        "Location": interview_location if interview_mode == "In-person" else "N/A"
    }
    st.session_state["schedule"].append(interview_details)
    st.success(f"Interview scheduled for {candidate_name} on {interview_date} at {interview_time}.")

# Display scheduled interviews
if st.session_state["schedule"]:
    st.header("Scheduled Interviews")
    df = pd.DataFrame(st.session_state["schedule"])
    st.dataframe(df)

# Option to clear schedule
if st.button("Clear Schedule"):
    st.session_state["schedule"] = []
    st.success("Interview schedule cleared.")
