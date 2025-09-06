# agent_orchestrator.py
import traceback
import logging
from crewai import Crew, Task
from crewai_agents import get_agents
from utils.azure_openai import call_azure_openai

# Set up logging for better debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load all registered CrewAI agents
agents = get_agents()

def identify_intent(user_input: str) -> str:
    """
    Uses Azure OpenAI GPT-4o to classify the user's intent.
    Returns one of: 'content', 'coder', 'analyst', or 'general'
    """
    try:
        system_prompt = (
            "You are an AI assistant that classifies user requests into one of the following categories:\n"
            "1. content_writing\n2. coding\n3. data_analysis\n4. general_conversation\n\n"
            "Return only the category name."
        )
        result = call_azure_openai(system_prompt, user_input)
        intent = result.strip().lower()

        logger.debug(f"Raw intent result: {result}")
        logger.debug(f"Processed intent: {intent}")

        if "content" in intent:
            return "content"
        elif "code" in intent or "program" in intent:
            return "coder"
        elif "data" in intent or "analysis" in intent:
            return "analyst"
        else:
            return "general"
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Intent Detection Error: {e}\nTraceback:\n{error_details}")
        return "general"  # fallback to general conversation

def create_task_for_intent(intent: str, user_input: str) -> Task:
    """
    Creates a properly structured task based on the intent
    """
    agent = agents.get(intent)
    if not agent:
        raise ValueError(f"No agent found for intent: {intent}")
    
    # Create more specific task descriptions and expected outputs
    if intent == "content":
        description = f"Create high-quality written content based on this request: {user_input}"
        expected_output = "A well-written piece of content that directly addresses the user's request, formatted appropriately and ready to use."
    elif intent == "coder":
        description = f"Generate clean, functional code to solve this programming request: {user_input}"
        expected_output = "Working code with proper comments and explanations, formatted correctly and ready to execute."
    elif intent == "analyst":
        description = f"Analyze the following data or provide data analysis insights: {user_input}"
        expected_output = "A clear analysis with key insights, trends, and actionable conclusions based on the provided information."
    else:
        description = f"Respond to this general request: {user_input}"
        expected_output = "A helpful and informative response that addresses the user's question or request."
    
    return Task(
        description=description,
        agent=agent,
        expected_output=expected_output
    )

def handle_user_input(user_input: str) -> str:
    """
    Handles user input, detects the intent, and invokes the appropriate agent or fallback model.
    Returns the assistant's response.
    """
    try:
        logger.info(f"Processing user input: {user_input[:100]}...")
        
        # Step 1: Detect user intent
        intent = identify_intent(user_input)
        logger.info(f"Detected intent: {intent}")

        # Step 2: Handle general conversation
        if intent == "general":
            logger.info("Handling as general conversation")
            return call_azure_openai(
                "You are an intelligent and friendly assistant that can both chat and assist with tasks using special expert agents.\n\n"
                "Here are the agents you can activate:\n"
                "- 'Content Writer' to create blogs, summaries, or articles.\n"
                "- 'Code Generator' to write and debug code in Python, React, etc.\n"
                "- 'Data Analyst' to analyze numbers, patterns, or datasets.\n\n"
                "If the user's message looks like a task request, you may suggest activating the appropriate agent or ask for clarification.\n"
                "If it's just a chat, respond normally.\n"
                "Don't try to do the agent's job directly—just guide or suggest agent help.\n\n"
                "Always keep your tone clear, casual, and helpful.",
                user_input
            )

        # Step 3: Validate agent exists
        agent = agents.get(intent)
        if not agent:
            logger.error(f"No agent found for intent: {intent}")
            return "⚠️ Sorry, I couldn't find the right agent for this task."

        logger.info(f"Using agent: {agent.role}")

        # Step 4: Create task with proper structure
        try:
            task = create_task_for_intent(intent, user_input)
            logger.debug(f"Created task - Description: {task.description[:100]}...")
            logger.debug(f"Expected output: {task.expected_output[:100]}...")
            
            # Step 5: Create and run the Crew
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True
            )
            
            logger.info("Starting crew execution...")
            result = crew.kickoff()
            logger.info("Crew execution completed successfully")
            logger.debug(f"Result type: {type(result)}")
            logger.debug(f"Result: {str(result)[:200]}...")
            
            # Handle different result types
            if hasattr(result, 'raw'):
                return str(result.raw)
            elif hasattr(result, 'output'):
                return str(result.output)
            else:
                return str(result)

        except Exception as agent_err:
            error_details = traceback.format_exc()
            logger.error(f"Crew Execution Error: {agent_err}\nTraceback:\n{error_details}")
            
            # Provide more specific error information
            error_msg = str(agent_err)
            if "tool" in error_msg.lower():
                return f"⚠️ Tool execution failed: {error_msg}. Please check your tool implementation."
            elif "task" in error_msg.lower():
                return f"⚠️ Task execution failed: {error_msg}. Please verify the task structure."
            else:
                return f"⚠️ Agent failed: {error_msg}. Please try rephrasing your request."

    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"General Orchestrator Error: {e}\nTraceback:\n{error_details}")
        return f"⚠️ System error occurred: {str(e)}. Please try again or contact support."