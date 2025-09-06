import streamlit as st
import os
import json
import csv
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI
import time
from pathlib import Path
import re
import glob

# Load environment variables from .env file (if exists)
try:
    load_dotenv()
except Exception as e:
    print(f"Error loading .env file: {str(e)}")

# Configuration for the app
st.set_page_config(page_title="FAQ Chatbot", layout="wide", initial_sidebar_state="auto")

# Initialize session state variables
if "conversations" not in st.session_state:
    st.session_state.conversations = {"New Chat": []}
    
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = "New Chat"

if "conversation_counter" not in st.session_state:
    st.session_state.conversation_counter = 1
    
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = []

if "api_key_configured" not in st.session_state:
    st.session_state.api_key_configured = False
    
if "api_endpoint_configured" not in st.session_state:
    st.session_state.api_endpoint_configured = False
    
if "deployment_name_configured" not in st.session_state:
    st.session_state.deployment_name_configured = False

# Knowledge base functions
def load_knowledge_base_from_file(file_path):
    """Load knowledge base from various file formats"""
    if not os.path.exists(file_path):
        return []
    
    file_extension = file_path.split('.')[-1].lower()
    content = []
    
    try:
        if file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                string_data = file.read()
                # Split by double newline to separate QA pairs
                pairs = string_data.split('\n\n')
                for pair in pairs:
                    parts = pair.split('\n', 1)
                    if len(parts) == 2:
                        question = parts[0].strip()
                        answer = parts[1].strip()
                        if question and answer:
                            content.append({"question": question, "answer": answer})
                        
        elif file_extension == 'csv':
            df = pd.read_csv(file_path)
            if 'question' in df.columns and 'answer' in df.columns:
                for _, row in df.iterrows():
                    content.append({"question": row['question'], "answer": row['answer']})
        
        # Add support for Excel files
        elif file_extension in ['xlsx', 'xls']:
            try:
                # First try with openpyxl engine (for .xlsx files)
                df = pd.read_excel(file_path, engine='openpyxl')
            except Exception:
                try:
                    # If that fails, try with xlrd engine (for .xls files)
                    df = pd.read_excel(file_path, engine='xlrd')
                except Exception as e:
                    st.error(f"Failed to read Excel file with both engines: {str(e)}")
                    return []
                    
            if 'question' in df.columns and 'answer' in df.columns:
                for _, row in df.iterrows():
                    # Handle potential NaN values
                    question = str(row['question']) if not pd.isna(row['question']) else ""
                    answer = str(row['answer']) if not pd.isna(row['answer']) else ""
                    if question and answer:  # Only add if both fields have content
                        content.append({"question": question, "answer": answer})
                    
        elif file_extension in ['json', 'jsonl']:
            with open(file_path, 'r', encoding='utf-8') as file:
                string_data = file.read()
                if file_extension == 'jsonl':
                    # Process JSON Lines
                    for line in string_data.splitlines():
                        if line.strip():
                            item = json.loads(line)
                            if 'question' in item and 'answer' in item:
                                content.append({"question": item['question'], "answer": item['answer']})
                else:
                    # Process regular JSON
                    data = json.loads(string_data)
                    if isinstance(data, list):
                        for item in data:
                            if 'question' in item and 'answer' in item:
                                content.append({"question": item['question'], "answer": item['answer']})
                            
        return content
    except Exception as e:
        st.error(f"Error loading knowledge base from {file_path}: {str(e)}")
        return []

# Load knowledge base from a directory
def load_knowledge_base_from_directory(directory="C:\\Users\\amudh\\OneDrive\\Desktop\\MindX\\MindX_Services\\Task_1\\knowledge_base"):
    """Load all knowledge base files from a directory"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        st.info(f"Created knowledge base directory: {directory}")
        return []
    
    content = []
    
    # Get all supported files in the directory
    file_patterns = [
        os.path.join(directory, "*.json"),
        os.path.join(directory, "*.jsonl"),
        os.path.join(directory, "*.csv"),
        os.path.join(directory, "*.txt"),
        os.path.join(directory, "*.xlsx"),  
        os.path.join(directory, "*.xls")
    ]
    
    
    files = []
    for pattern in file_patterns:
        pattern_files = glob.glob(pattern)
        files.extend(pattern_files)
        #st.sidebar.write(f"Found {len(pattern_files)} {pattern.split('*')[-1]} files")
    
    #st.sidebar.write(f"Total files found: {len(files)}")
    
    for file_path in files:
        #st.sidebar.write(f"Processing: {os.path.basename(file_path)}")
        file_content = load_knowledge_base_from_file(file_path)
        if file_content:
            content.extend(file_content)
            #st.sidebar.success(f"✓ Loaded {len(file_content)} Q&A pairs from {os.path.basename(file_path)}")
        #else:
            #st.sidebar.error(f"✗ Failed to load {os.path.basename(file_path)}")
    
    return content


def search_knowledge_base(query, knowledge_base):
    """Search knowledge base for relevant entries"""
    if not knowledge_base:
        return []
    
    query = query.lower()
    results = []
    
    for entry in knowledge_base:
        question = entry["question"].lower()
        # Simple keyword matching
        if any(word in question for word in query.split()):
            results.append(entry)
    
    return results

# Azure OpenAI API functions
def initialize_azure_client():
    """Initialize Azure OpenAI client with session variables or environment variables"""
    try:
        # Try to get API key from .env file if not set in session
        api_key = st.session_state.get("api_key") or os.getenv("AZURE_OPENAI_API_KEY")
        api_endpoint = st.session_state.get("api_endpoint") or os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = st.session_state.get("deployment_name") or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        # Update session state with environment variables if found
        if not st.session_state.get("api_key") and api_key:
            st.session_state.api_key = api_key
            st.session_state.api_key_configured = True
            
        if not st.session_state.get("api_endpoint") and api_endpoint:
            st.session_state.api_endpoint = api_endpoint
            st.session_state.api_endpoint_configured = True
            
        if not st.session_state.get("deployment_name") and deployment_name:
            st.session_state.deployment_name = deployment_name
            st.session_state.deployment_name_configured = True
        
        if api_key and api_endpoint and deployment_name:
            client = AzureOpenAI(
                api_key=api_key,
                api_version="2024-12-01-preview",
                azure_endpoint=api_endpoint
            )
            return client
            
        if not api_key:
            st.warning("Azure OpenAI API Key not found. Please add it to your .env file as AZURE_OPENAI_API_KEY or enter it in the sidebar.")
        if not api_endpoint:
            st.warning("Azure Endpoint not found. Please add it to your .env file as AZURE_OPENAI_ENDPOINT or enter it in the sidebar.")
        if not deployment_name:
            st.warning("Deployment Name not found. Please add it to your .env file as AZURE_OPENAI_DEPLOYMENT_NAME or enter it in the sidebar.")
            
        return None
    except Exception as e:
        st.error(f"Error initializing Azure OpenAI client: {str(e)}")
        return None

def get_ai_response(client, messages, knowledge_base_context=""):
    """Get response from Azure OpenAI API"""
    if not client:
        return "API client not configured properly. Please check your settings."
    
    try:
        # Prepare system message with knowledge base context
        system_message = {
            "role": "system", 
            "content": f"You are a helpful FAQ assistant. Your responses should be concise and informative. Use the knowledge base information when available: {knowledge_base_context}"
        }
        
        # Combine system message with conversation history
        full_messages = [system_message] + messages
        
        # Get completion from Azure OpenAI
        response = client.chat.completions.create(
            model=st.session_state.deployment_name,
            messages=full_messages,
            temperature=0.7,
            max_tokens=800,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response from AI: {str(e)}"

# UI Helper functions
def handle_chat_input(prompt):
    """Process user input and get AI response"""
    if not prompt:
        return
    
    # Get current conversation messages
    current_messages = st.session_state.conversations[st.session_state.current_conversation]
    
    # Add user message to chat history
    current_messages.append({"role": "user", "content": prompt})
    
    # Search knowledge base for relevant information
    relevant_entries = search_knowledge_base(prompt, st.session_state.knowledge_base)
    knowledge_context = ""
    
    if relevant_entries:
        knowledge_context = "Relevant FAQ information:\n" + "\n".join([
            f"Q: {entry['question']}\nA: {entry['answer']}" 
            for entry in relevant_entries[:3]  # Limit to top 3 matches
        ])
    
    # Initialize client
    client = initialize_azure_client()
    
    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        ai_response = get_ai_response(
            client, 
            [msg for msg in current_messages if msg["role"] != "system"],
            knowledge_context
        )
        
        # Simulate typing
        full_response = ""
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.01)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(ai_response)
    
    # Add assistant response to chat history
    current_messages.append({"role": "assistant", "content": ai_response})
    # Update the conversation in session state
    st.session_state.conversations[st.session_state.current_conversation] = current_messages

def create_new_chat():
    """Create a new conversation"""
    chat_name = f"New Chat {st.session_state.conversation_counter}"
    st.session_state.conversations[chat_name] = []
    st.session_state.current_conversation = chat_name
    st.session_state.conversation_counter += 1
    
def switch_conversation(conversation_name):
    """Switch to another conversation"""
    st.session_state.current_conversation = conversation_name

def check_api_configuration():
    """Check if the API is configured correctly"""
    st.session_state.api_key_configured = bool(st.session_state.get("api_key", ""))
    st.session_state.api_endpoint_configured = bool(st.session_state.get("api_endpoint", ""))
    st.session_state.deployment_name_configured = bool(st.session_state.get("deployment_name", ""))
    
    return (st.session_state.api_key_configured and 
            st.session_state.api_endpoint_configured and 
            st.session_state.deployment_name_configured)

# Custom CSS to make the app look more like ChatGPT
def apply_custom_css():
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    
    .chatbox {
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #f7f7f8;
    }
    
    .assistant-message {
        background-color: #ffffff;
    }
    
    .chat-input {
        position: fixed;
        bottom: 3rem;
        width: 60%;
    }
    
    .sidebar .block-container {
        padding-top: 2rem;
    }
    
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
    }
    
    .stButton>button {
        border-radius: 0.5rem;
        width: 100%;
        text-align: left;
        word-wrap: break-word;
        white-space: normal;
        height: auto;
        min-height: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Custom header for the sidebar */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    /* Make the New Chat button look like the one in ChatGPT */
    .new-chat-btn {
        background-color: #202123;
        color: white;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        cursor: pointer;
        text-align: center;
    }
    
    /* Styling for the knowledge base section */
    .kb-header {
        font-size: 1.25rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Style for conversation buttons in sidebar */
    button[data-testid="baseButton-secondary"] {
        background-color: transparent;
        border: 1px solid #e0e0e0;
        text-align: left;
        font-size: 0.9rem;
        transition: background-color 0.3s;
    }
    
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    apply_custom_css()
    
    # Load knowledge base from project directory at startup
    if len(st.session_state.knowledge_base) == 0:
        st.session_state.knowledge_base = load_knowledge_base_from_directory()
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">FAQ Chatbot</div>', unsafe_allow_html=True)
        
        # New Chat button
        if st.button("New Chat", key="new_chat"):
            create_new_chat()
            st.rerun()
        
        # Conversation history
        st.markdown('<div class="kb-header">Conversations</div>', unsafe_allow_html=True)
        
        # Display conversation list
        for conv_name in st.session_state.conversations.keys():
            # Check if this conversation has messages
            conv_messages = st.session_state.conversations[conv_name]
            first_message = "New conversation" if not conv_messages else conv_messages[0]["content"][:20] + "..."
            
            # Format the conversation button
            button_style = "background-color: #f0f2f6;" if conv_name == st.session_state.current_conversation else ""
            
            if st.button(
                f"{conv_name}\n{first_message}", 
                key=f"conv_{conv_name}",
                use_container_width=True,
                disabled=conv_name == st.session_state.current_conversation
            ):
                switch_conversation(conv_name)
                st.rerun()
        
        # Azure OpenAI API Configuration
        st.markdown('<div class="kb-header">API Configuration</div>', unsafe_allow_html=True)
        
        # Check if API keys are already set in environment variables
        env_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        env_api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        env_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
        
        if env_api_key and env_api_endpoint and env_deployment_name:
            st.success("API configuration found in environment variables!")
            st.session_state.api_key = env_api_key
            st.session_state.api_endpoint = env_api_endpoint
            st.session_state.deployment_name = env_deployment_name
            check_api_configuration()
        else:
            # Show input fields only if not configured in environment
            api_key = st.text_input(
                "Azure OpenAI API Key", 
                type="password",
                value=st.session_state.get("api_key", ""),
                key="api_key_input"
            )
            
            api_endpoint = st.text_input(
                "Azure Endpoint", 
                value=st.session_state.get("api_endpoint", ""),
                key="api_endpoint_input"
            )
            
            deployment_name = st.text_input(
                "Deployment Name", 
                value=st.session_state.get("deployment_name", ""),
                key="deployment_name_input"
            )
            
            if st.button("Save API Configuration"):
                st.session_state.api_key = api_key
                st.session_state.api_endpoint = api_endpoint
                st.session_state.deployment_name = deployment_name
                check_api_configuration()
                st.success("API configuration saved!")
        
        # Show knowledge base statistics
        st.markdown('<div class="kb-header">Knowledge Base</div>', unsafe_allow_html=True)
        if st.session_state.knowledge_base:
            st.markdown(f"Loaded: {len(st.session_state.knowledge_base)} Q&A pairs")
        else:
            st.warning("No knowledge base loaded. Please check the 'knowledge_base' directory.")
            
        # Reload knowledge base button
        if st.button("Reload Knowledge Base"):
            st.session_state.knowledge_base = load_knowledge_base_from_directory()
            st.rerun()
    
    # Main chat area
    st.markdown("# FAQ Chatbot")
    
    # Check API configuration
    api_configured = check_api_configuration()
    if not api_configured:
        st.warning("Please configure the Azure OpenAI API in the sidebar or add the necessary environment variables.")
    
    # Display current conversation messages
    current_messages = st.session_state.conversations[st.session_state.current_conversation]
    for idx, message in enumerate(current_messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question...", key="chat_input", disabled=not api_configured):
        handle_chat_input(prompt)

if __name__ == "__main__":
    main()
