from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")

# Apply custom CSS for coloring and styling
st.markdown(
    """
    <style>
    .header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
    }
    .subheader {
        color: #FFA500;
        font-size: 1.5rem;
    }
    .input-box {
        font-size: 1.25rem;
        color: #000080;
    }
    .chat-history {
        font-size: 1rem;
        color: #4A4A4A;
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page header
st.markdown("<div class='header'>AI Assistant</div>", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input text box with style
input = st.text_input("Input: ", key="input", placeholder="Ask a question...", help="Type your query here", label_visibility="collapsed")

submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    
    # Display the AI response
    st.markdown("<div class='subheader'>The Response is:</div>", unsafe_allow_html=True)
    
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.markdown("<div class='subheader'>The Chat History is:</div>", unsafe_allow_html=True)
    
for role, text in st.session_state['chat_history']:
    st.markdown(f"<div class='chat-history'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
