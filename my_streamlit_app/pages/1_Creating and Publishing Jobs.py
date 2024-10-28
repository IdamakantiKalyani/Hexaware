import streamlit as st
from datetime import date
import pandas as pd

st.title("Creating and Publishing Jobs")

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access the Creating and Publishing Jobs page.")
    st.stop()

# Initialize data
if 'draft_jobs' not in st.session_state:
    st.session_state['draft_jobs'] = []
if 'published_jobs' not in st.session_state:
    st.session_state['published_jobs'] = []

# Create or Edit Job Form
def job_form(job=None, is_edit=False, job_list=None):
    st.write("Edit Job" if is_edit else "Create Job")
    job_title = st.text_input("Job Title", value=job.get("title") if job else "")
    job_description = st.text_area("Job Description", value=job.get("description") if job else "", help="Min 50 characters")
    department = st.selectbox("Department", ["HR", "IT", "Marketing", "Sales"], index=["HR", "IT", "Marketing", "Sales"].index(job.get("department")) if job else 0)
    job_location = st.text_input("Job Location", value=job.get("location") if job else "")
    employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract", "Internship"], index=["Full-time", "Part-time", "Contract", "Internship"].index(job.get("employment")) if job else 0)
    salary_min = st.number_input("Min Salary", value=job.get("salary_min") if job else 0, step=1000)
    salary_max = st.number_input("Max Salary", value=job.get("salary_max") if job else 0, step=1000)
    deadline = st.date_input("Application Deadline", value=job.get("deadline") if job else date.today(), min_value=date.today())
    required_qualifications = st.text_area("Required Qualifications", value=job.get("qualifications") if job else "")
    preferred_qualifications = st.text_area("Preferred Qualifications", value=job.get("preferred") if job else "")
    responsibilities = st.text_area("Responsibilities", value=job.get("responsibilities") if job else "")

    # Save as Draft or Publish
    if st.button("Save as Draft"):
        job_data = {"title": job_title, "description": job_description, "department": department, "location": job_location, "employment": employment_type, "salary_min": salary_min, "salary_max": salary_max, "deadline": deadline, "qualifications": required_qualifications, "preferred": preferred_qualifications, "responsibilities": responsibilities}
        if is_edit:
            job_list.remove(job)
        st.session_state["draft_jobs"].append(job_data)
        st.success("Saved as draft.")
    if st.button("Publish"):
        job_data = {"title": job_title, "description": job_description, "department": department, "location": job_location, "employment": employment_type, "salary_min": salary_min, "salary_max": salary_max, "deadline": deadline, "qualifications": required_qualifications, "preferred": preferred_qualifications, "responsibilities": responsibilities, "status": "Published"}
        if is_edit:
            job_list.remove(job)
        st.session_state["published_jobs"].append(job_data)
        st.success("Job published.")

# Draft Jobs Screen
def draft_jobs_screen():
    st.write("Draft Jobs")
    for job in st.session_state["draft_jobs"]:
        col1, col2 = st.columns([3, 1])
        col1.write(f"**{job['title']} - {job['department']}**")
        if col2.button("Edit", key=f"edit_{job['title']}"):
            job_form(job, is_edit=True, job_list=st.session_state["draft_jobs"])

# Published Jobs Screen
def published_jobs_screen():
    st.write("Published Jobs")
    for job in st.session_state["published_jobs"]:
        col1, col2 = st.columns([3, 1])
        col1.write(f"**{job['title']} - {job['department']}**")
         # Sidebar Navigation
st.sidebar.title("Recruitment Assist")
page = st.sidebar.radio("Go to", ["Create Job", "Draft Jobs", "Published Jobs"])
if page == "Create Job":
    job_form()
elif page == "Draft Jobs":
    draft_jobs_screen()
elif page == "Published Jobs":
    published_jobs_screen()
