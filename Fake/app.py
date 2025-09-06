import streamlit as st
import requests
import os

# Streamlit Page Setup
st.set_page_config(page_title="🛒 E-Commerce ChatBot", layout="wide")
st.title("🛍️ E-Commerce ChatBot")

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/chat")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
user_input = st.chat_input("Ask me about products or carts!")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare payload
    payload = {
        "thread_id": st.session_state.thread_id,
        "messages": [{"role": "user", "content": user_input}]
    }

    # Call FastAPI backend
    try:
        response = requests.post(BACKEND_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        st.session_state.thread_id = data.get("thread_id")
        assistant_response = data.get("content", "No response.")

    except Exception as e:
        assistant_response = f"Error contacting backend: {e}"

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response, unsafe_allow_html=True)
