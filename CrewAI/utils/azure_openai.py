# utils/azure_openai.py
# Utility module to call Azure OpenAI GPT-4o

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env
load_dotenv()

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
)

def call_azure_openai(system_prompt: str, user_input: str) -> str:
    """
    Calls Azure OpenAI's GPT-4o with a system prompt and user input.
    Returns: The model's response as a string.
    """
    try:
        print("[AzureOpenAI] Sending request to Azure OpenAI...")
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        print("[AzureOpenAI] Received response successfully.")
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Azure OpenAI call failed: {str(e)}")
        return f"[Azure OpenAI Error] {str(e)}"
        