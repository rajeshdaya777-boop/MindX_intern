# main.py
import streamlit as st
import logging
import sys
from agent_orchestrator import handle_user_input

# Configure logging to show in Streamlit
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(page_title="Multi-Agent Chatbot", page_icon="🤖")
st.title("🤖 AI Assistant with CrewAI Agents")

# Add debug mode toggle
debug_mode = st.sidebar.checkbox("Debug Mode", value=False)
if debug_mode:
    st.sidebar.write("Debug mode is ON - check console for detailed logs")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display system status
with st.sidebar:
    st.header("System Status")
    try:
        from crewai_agents import get_agents
        agents = get_agents()
        st.success(f"✅ {len(agents)} agents loaded")
        for intent, agent in agents.items():
            st.write(f"- {intent}: {agent.role}")
    except Exception as e:
        st.error(f"❌ Agent loading failed: {str(e)}")
        if debug_mode:
            st.code(str(e))

# Chat input
user_input = st.chat_input("Ask me anything...", key="user_input")

# If user submits input
if user_input:
    try:
        logger.info(f"User input received: {user_input}")
        
        # Add user message to history
        st.session_state.chat_history.append(("user", user_input))

        # Show processing indicator
        with st.spinner("Processing your request..."):
            # Get chatbot response
            response = handle_user_input(user_input)
            logger.info("Response generated successfully")

        # Add bot response to history
        st.session_state.chat_history.append(("assistant", response))
        
    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        logger.error(f"Main error: {e}")
        st.session_state.chat_history.append(("assistant", error_msg))
        
        if debug_mode:
            st.error("Debug Info:")
            st.code(str(e))

# Display chat history
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)

# Add clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()