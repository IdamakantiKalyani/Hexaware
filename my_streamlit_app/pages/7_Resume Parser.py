import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the Gemini AI response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Input prompt template
input_prompt = """
Welcome to the AI-Powered Resume Parser!

Easily upload your resume and job description to receive personalized insights on how well your resume matches the job. Our advanced system analyzes key qualifications, highlights missing skills, and provides targeted recommendations to improve your chances of landing the job. Whether you're aiming to optimize your profile or tailor it for a specific role, this tool offers detailed feedback, including:

--> Job Description Match Percentage
--> Relevant Keywords Found
--> Missing Keywords
--> Profile Summary Suggestions

Make your resume stand out in a competitive job market!

resume:{text}
description:{jd}

I want the response in one single string having the structure JD Percentage Match(highlighted bold text): next line  Matching Keywords which are in resume information then  in next line missing keywords(Highlighted bold text) with pointwise but short and concise and next line with spaces for profile summary listed in resume information and at last give some recommendations.
"""

# Streamlit sidebar
st.sidebar.title("🔍 **Advanced Resume Tracking System**")
st.sidebar.markdown("<p style='color: #008080;'>Improve Your Resume Right now!</p>", unsafe_allow_html=True)
jd = st.sidebar.text_area("📄 Paste the Job Description", 
                          placeholder="Input the job description for matching or get profile review recommendations.")
uploaded_file = st.sidebar.file_uploader("📂 Upload Your Resume", type="pdf", help="Please upload the PDF format only.")

submit = st.sidebar.button("🚀 Submit")

# Main app content
if uploaded_file is None:
    st.markdown("<h1 style='color: #4CAF50;'>Resume Parsing System</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2rem;'>Welcome to the Resume Parsing System! Upload your job description and resume to get a match percentage, missing skills, and recommendations.</p>", unsafe_allow_html=True)
    st.markdown("Click the buttons below to visit LinkedIn, GitHub, or Google.")
    
    # Social media buttons
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/idamakanti-siva-kalyani-4237bb268/")
    with col2:
        st.link_button("GitHub", "https://github.com/IdamakantiKalyani")
    with col3:
        st.link_button("Google", "https://www.google.com/")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.info('💼 Resume Tracking - Making Job Applications Easier!', icon=None)
    st.warning('⚠️ Upload Resume in .pdf format only.')

# Process PDF and job description on submit
if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        space = "                                                      "
        response = get_gemini_response(text + " as resume information " + space + jd + " as job description " + space + input_prompt)
        st.markdown("<h2 style='color: #FF4500;'>AI Response:</h2>", unsafe_allow_html=True)
        st.markdown(f"<p>{response}</p>", unsafe_allow_html=True)
