from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import json
import re
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv
from metrics import metrics
from utils import fetch_data

# Load environment variables
load_dotenv()

app = FastAPI()

# Azure OpenAI config
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_URL"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY_COM"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION_PRE", "2025-03-01-preview")
)

assistant = client.beta.assistants.create(
    name="Chat Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "fetch_data",
                "description": "Fetch or simulate update of user data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "method": {
                            "type": "string",
                            "enum": ["GET", "POST", "PUT"]
                        },
                        "updates": {
                            "type": "object",
                            "additionalProperties": True
                        }
                    },
                    "required": ["user_id", "method"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_products",
                "description": "Get all product details from the FakeStore API.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ]
)

assistant_id = assistant.id

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    thread_id: Optional[str] = None
    messages: List[Message]

class ChatResponse(BaseModel):
    thread_id: str
    message_id: str
    role: str
    content: Optional[str]

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Create or reuse a thread
        thread_id = request.thread_id or client.beta.threads.create().id

        # Post all user messages
        for message in request.messages:
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role=message.role,
                content=message.content
            )

        # Run assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        if run.status == "requires_action":
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                func = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if func == "fetch_data":
                    payload = args.get("updates", {})
                    if "user_id" in args and "user_id" not in payload:
                        payload["user_id"] = args["user_id"]

                    endpoint = metrics[func]["url"]
                    base_url = metrics[func]["base_url"]

                    if 'user_id' in payload:
                        endpoint = endpoint.replace("{user_id}", str(payload["user_id"]))

                    print("Function arguments:", args)
                    print("Payload before fetch_data:", payload)
                    print("Final endpoint:", endpoint)

                    try:
                        result = fetch_data(
                            method=args.get("method", metrics[func]["method"]), 
                            endpoint=endpoint,
                            base_url=base_url,
                            json_payload=payload
                        )

                        if not result or not isinstance(result, dict) or "id" not in result:
                            result = {"message": "User data not found or API failed."}

                        print("Result being sent to assistant:", result)

                    except Exception as e:
                        print("Error in fetch_data:", e)
                        result = {"message": f"Error fetching user data: {str(e)}"}

                elif func == "get_products":
                    endpoint = metrics[func]["url"]
                    base_url = metrics[func]["base_url"]

                    try:
                        result = fetch_data(
                            method=metrics[func]["method"],
                            endpoint=endpoint,
                            base_url=base_url
                        )

                        if not result or "products" not in result:
                            result = {"message": "No products found or API failed."}
                        else:
                            products = result["products"][:5]  # Show first 5 products
                            formatted = "\n\n".join(
                                f"**{p['title']}**\nBrand: {p['brand']}\nCategory: {p['category']}\nPrice: ${p['price']}\nRating: {p['rating']}/5"
                                for p in products
                            )
                            result = {"message": f"Here are some product details:\n\n{formatted}"}

                        print("Product result being sent to assistant:", result)

                    except Exception as e:
                        print("Error in get_products:", e)
                        result = {"message": f"Error fetching product data: {str(e)}"}

                else:
                    result = {"message": "Unknown function"}

                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(result)
                })

            # Submit tool outputs and continue execution
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            except Exception as e:
                print("Error in submitting tool outputs:", e)
                raise HTTPException(status_code=500, detail=f"Error submitting tool outputs: {str(e)}")

        # Fetch final assistant message
        messages = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=10)
        for msg in messages.data:
            if msg.role == "assistant" and hasattr(msg, "content") and msg.content:
                content = (
                    msg.content[0].text.value if isinstance(msg.content, list) else msg.content
                )
                cleaned = re.sub(r"【\d+:\d+†source】", "", content)
                return ChatResponse(
                    thread_id=thread_id,
                    message_id=msg.id,
                    role="assistant",
                    content=cleaned
                )

        raise HTTPException(status_code=404, detail="No valid assistant message found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")
