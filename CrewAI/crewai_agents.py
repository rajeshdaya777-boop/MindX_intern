from crewai import Agent
from custom_tools import get_tools
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Azure OpenAI LLM setup
llm = AzureOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# Get tools for each agent
tools = get_tools()

def get_agents():
    content_writer = Agent(
        role="Content Writer",
        goal="Generate high-quality SEO content",
        backstory="An experienced writer with SEO expertise",
        tools=tools['content'],
        llm=llm,
        verbose=True
    )

    coder = Agent(
        role="Python Developer",
        goal="Solve coding problems and write clean code",
        backstory="A developer proficient in Python and software engineering",
        tools=tools['coder'],
        llm=llm,
        verbose=True
    )

    analyst = Agent(
        role="Data Analyst",
        goal="Analyze and interpret data effectively",
        backstory="An analyst skilled in extracting insights from data",
        tools=tools['analyst'],
        llm=llm,
        verbose=True
    )

    return {
        "content": content_writer,
        "coder": coder,
        "analyst": analyst
    }
