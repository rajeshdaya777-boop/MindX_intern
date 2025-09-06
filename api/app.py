# app.py
import streamlit as st
import requests

st.title("🧠 Chat Assistant")

API_URL = "http://localhost:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Say something...")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Send user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "messages": st.session_state.messages[-5:]  # send last 5 messages
    }

    with st.spinner("Thinking..."):
        try:
            res = requests.post(API_URL, json=payload)
            res.raise_for_status()
            data = res.json()
            
            # Check if 'content' exists in the response and display it
            reply = data.get("content", "")
            if reply:
                st.session_state.messages.append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.markdown(reply)
            else:
                st.error("No response content available.")

        except Exception as e:
            st.error(f"Error: {e}")
