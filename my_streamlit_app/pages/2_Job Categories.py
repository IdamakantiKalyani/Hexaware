import streamlit as st
import sqlite3
st.title("Job Categories")

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access the Job Categories page.")
    st.stop()

# Database setup for job categories
def create_job_categories_db():
    conn = sqlite3.connect('job_categories.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS job_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_type TEXT NOT NULL,
            category_name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a new category to the database
def add_category(category_type, category_name):
    conn = sqlite3.connect('job_categories.db')
    c = conn.cursor()
    c.execute('INSERT INTO job_categories (category_type, category_name) VALUES (?, ?)', (category_type, category_name))
    conn.commit()
    conn.close()

# Fetch all categories from the database
def get_all_categories():
    conn = sqlite3.connect('job_categories.db')
    c = conn.cursor()
    c.execute('SELECT * FROM job_categories')
    categories = c.fetchall()
    conn.close()
    return categories

# Update a category in the database
def update_category(category_id, category_type, category_name):
    conn = sqlite3.connect('job_categories.db')
    c = conn.cursor()
    c.execute('UPDATE job_categories SET category_type = ?, category_name = ? WHERE id = ?', 
              (category_type, category_name, category_id))
    conn.commit()
    conn.close()

# Delete a category from the database
def delete_category(category_id):
    conn = sqlite3.connect('job_categories.db')
    c = conn.cursor()
    c.execute('DELETE FROM job_categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()

# Initialize database
create_job_categories_db()

# Job Categories Management Screen
st.title("Job Categories Management")

st.subheader("Add New Category")
category_type = st.selectbox("Category Type", ["Department", "Location", "Employment Type"], index=0, key="category_type_dropdown")
category_name = st.text_input("Category Name", placeholder="Enter the category name", key="category_name_textbox")

if st.button("Add Category"):
    if category_type and category_name:
        add_category(category_type, category_name)
        st.success(f"Category '{category_name}' added under '{category_type}'!")
    else:
        st.error("Both fields are required")

st.subheader("Existing Categories")
categories = get_all_categories()
if categories:
    for category in categories:
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        col1.write(category[0])  # ID
        col2.write(category[1])  # Category Type
        col3.write(category[2])  # Category Name
        edit = col4.button("Edit", key=f"edit_{category[0]}")
        delete = col4.button("Delete", key=f"delete_{category[0]}")

        # Handle Edit button
        if edit:
            with st.modal("Edit Category"):
                new_type = st.selectbox("Edit Category Type", ["Department", "Location", "Employment Type"], index=0)
                new_name = st.text_input("Edit Category Name", category[2])
                if st.button("Save Changes"):
                    update_category(category[0], new_type, new_name)
                    st.success("Category updated successfully!")

        # Handle Delete button
        if delete:
            delete_category(category[0])
            st.warning(f"Category '{category[2]}' deleted.")

# Job Creation Screen with Categories Integration
st.title("Job Creation")
st.subheader("Assign Categories to Job Posting")

departments = [c[2] for c in get_all_categories() if c[1] == "Department"]
locations = [c[2] for c in get_all_categories() if c[1] == "Location"]
employment_types = [c[2] for c in get_all_categories() if c[1] == "Employment Type"]

department = st.selectbox("Department", options=departments, index=0)
job_location = st.selectbox("Job Location", options=locations, index=0)
employment_type = st.selectbox("Employment Type", options=employment_types, index=0)

if st.button("Create Job"):
    st.success(f"Job created with Department: {department}, Location: {job_location}, Employment Type: {employment_type}")
