import streamlit as st
import sqlite3
st.title("Application Forms")
# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access the Application Forms Management.")
    st.stop()

# Allow only authorized roles
st.session_state.user_role = "Admin"
if st.session_state.user_role not in ["Admin"]:
    st.error("Only Admin have permission to access this page.")
    st.stop()

# Database connection
def create_connection():
    conn = sqlite3.connect('job_categories.db')
    return conn

# Create application forms table
def create_forms_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS application_forms (
                    form_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_name TEXT NOT NULL,
                    associated_job TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS form_fields (
                    field_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_id INTEGER NOT NULL,
                    field_name TEXT NOT NULL,
                    field_type TEXT NOT NULL,
                    field_options TEXT,
                    FOREIGN KEY (form_id) REFERENCES application_forms (form_id)
                )''')
    conn.commit()
    conn.close()

# Insert a new form
def insert_form(form_name, associated_job):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO application_forms (form_name, associated_job) VALUES (?, ?)', (form_name, associated_job))
    conn.commit()
    conn.close()

# Insert new fields for a form
def insert_form_field(form_id, field_name, field_type, field_options=None):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO form_fields (form_id, field_name, field_type, field_options)
                 VALUES (?, ?, ?, ?)''', (form_id, field_name, field_type, field_options))
    conn.commit()
    conn.close()

# Retrieve all forms
def get_all_forms():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM application_forms')
    forms = c.fetchall()
    conn.close()
    return forms

# Retrieve fields of a form
def get_form_fields(form_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM form_fields WHERE form_id = ?', (form_id,))
    fields = c.fetchall()
    conn.close()
    return fields

# Delete form by ID
def delete_form(form_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM form_fields WHERE form_id = ?', (form_id,))
    c.execute('DELETE FROM application_forms WHERE form_id = ?', (form_id,))
    conn.commit()
    conn.close()

# UI for managing application forms
def manage_forms():
   

    # Create the forms table if it doesn't exist
    create_forms_table()

    # Display existing forms
    st.subheader("Existing Forms")
    forms = get_all_forms()

    if forms:
        for form in forms:
            col1, col2, col3, col4 = st.columns([3, 3, 1, 1])
            col1.write(form[1])  # Form Name
            col2.write(form[2])  # Associated Job
            if col3.button("Edit", key=f"edit_{form[0]}"):
                edit_form(form)
            if col4.button("Delete", key=f"delete_{form[0]}"):
                delete_form(form[0])
                st.success(f"Form '{form[1]}' deleted successfully!")
                st.experimental_rerun()  # Refresh the page after deletion
    else:
        st.info("No forms available. Create a new form below.")

    # Form creation section
    st.subheader("Create New Application Form")
    form_name = st.text_input("Form Name", placeholder="Enter the form name")
    associated_job = st.text_input("Associated Job", placeholder="Enter the associated job")

    if st.button("Create Form"):
        if form_name and associated_job:
            insert_form(form_name, associated_job)
            st.success(f"Form '{form_name}' created successfully!")
            st.experimental_rerun()  # Refresh the page to show the new form
        else:
            st.error("Please fill out all fields.")

# UI for editing form
def edit_form(form):
    st.subheader(f"Editing Form: {form[1]}")
    form_name = st.text_input("Form Name", value=form[1])
    associated_job = st.text_input("Associated Job", value=form[2])

    if st.button("Save Changes", key=f"save_{form[0]}"):
        # Function to update the form (can be implemented similar to insert)
        st.success(f"Form '{form_name}' updated successfully!")

    # Add fields to the form
    st.subheader("Add Fields to Form")
    field_name = st.text_input("Field Name", placeholder="Enter field name")
    field_type = st.selectbox("Field Type", ["Textbox", "Dropdown", "Checkbox", "Radio Button", "Date Picker"])

    field_options = ""
    if field_type in ["Dropdown", "Checkbox", "Radio Button"]:
        field_options = st.text_area("Field Options", placeholder="Enter options separated by commas")

    if st.button("Add Field", key=f"add_field_{form[0]}"):
        insert_form_field(form[0], field_name, field_type, field_options)
        st.success(f"Field '{field_name}' added to form '{form[1]}'.")

    # Show current fields
    st.subheader("Current Fields")
    fields = get_form_fields(form[0])
    if fields:
        for field in fields:
            st.write(f"{field[1]} ({field[2]}) - Options: {field[3]}")
    else:
        st.info("No fields added yet.")

# Main function
if __name__ == "__main__":
    manage_forms()
