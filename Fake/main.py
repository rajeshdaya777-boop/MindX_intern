from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import json
import re
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Fetch Environment Variables
api_key = os.getenv("AZURE_OPENAI_API_KEY_COM")
api_version = os.getenv("AZURE_OPENAI_API_VERSION_PRE", "2025-03-01-preview")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_URL")
deployment_model = os.getenv("AZURE_DEPLOYMENT_MODEL")
assistant_id = os.getenv("AZURE_ASSISTANT_ID")  # Make sure this is set in your .env file

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

# Fetch Products from Fakestore API
def fetch_products():
    try:
        response = requests.get("https://fakestoreapi.com/products")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

# Pydantic Models
class Message(BaseModel):
    role: str
    content: str

class ActionDetails(BaseModel):
    url: str
    description: str
    method: str
    headers: Dict[str, str]
    content_type: str
    input: List[Dict]

class ChatRequest(BaseModel):
    thread_id: Optional[str] = None
    messages: List[Message]
    action_details: Optional[ActionDetails] = None

class ChatResponse(BaseModel):
    thread_id: str
    message_id: str
    role: str
    content: Optional[str]

# Chat Endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Create a thread if not provided
        thread_id = request.thread_id or client.beta.threads.create().id

        # Send user messages to thread
        for message in request.messages:
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role=message.role,
                content=message.content
            )

        # Run assistant and wait for completion
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # If assistant called a function, fulfill it
        if run.status == "requires_action":
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "get_products":
                    products = fetch_products()
                    output = {"products": [{"title": p["title"], "price": p["price"]} for p in products]}
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(output)  # Must be a string
                    })

            # Submit tool outputs and wait again
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        # Get final assistant message
        messages = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=10)
        for msg in messages.data:
            if msg.role == "assistant" and hasattr(msg, "content") and msg.content:
                response_text = (
                    msg.content[0].text.value if isinstance(msg.content, list) else msg.content
                )
                cleaned = re.sub(r"【\d+:\d+†source】", "", response_text)
                return ChatResponse(
                    thread_id=thread_id,
                    message_id=msg.id,
                    role="assistant",
                    content=cleaned
                )

        raise HTTPException(status_code=404, detail="No valid assistant message found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
