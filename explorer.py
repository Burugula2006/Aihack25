import streamlit as st
import google.generativeai as genai
from typing import Generator
st.set_page_config(layout="wide")
# Configure Gemini API

GOOGLE_API_KEY = "AIzaSyCVUVzWvtDc6tlldI2LuEjIKVAA5oQeH9Y"
genai.configure(api_key=GOOGLE_API_KEY)

# System Prompt (Defines chatbot behavior)
SYSTEM_PROMPT = """
You are Gemini AI, a location-based historical content generator. Your task is to create detailed historical summaries that cover the entire history of a user-specified location. Focus on key events, notable figures, cultural heritage, and architectural significance in a way that is accurate, engaging, and informative. Additionally, suggest local historical landmarks with a short paragraph describing their historical importance and why they are worth visiting. Include recommendations for related historical or cultural activities, such as museums, historical tours, or cultural experiences. Where possible, provide links to multimedia resources, such as images, maps, or virtual tours, to enhance the user’s experience. Provide citations or references for the historical information, but no specific citation style is required. Maintain a formal tone throughout your response.

"""


# Function to format chat history correctly
def format_messages(messages):
    formatted = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]  # Set system prompt role to "user"
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"  # Ensure correct roles
        formatted.append({"role": role, "parts": [{"text": msg["content"]}]})
    return formatted

# Function to generate chat responses
def gemini_generator(messages: list) -> Generator:
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=format_messages(messages))
    
    user_input = messages[-1]["content"]  
    response = chat.send_message(user_input, stream=True)

    for chunk in response:
        yield chunk.text

# Page title
st.title("The Explorer🗺")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f'<div class="chat-box user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f'<div class="chat-box assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input functionality
if prompt := st.chat_input("How can I assist you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-box user-message">{prompt}</div>', unsafe_allow_html=True)

    # Get response from Gemini
    with st.chat_message("assistant"):
        response = st.write_stream(gemini_generator(st.session_state.messages))
    
    # Save response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})