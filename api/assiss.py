# # main.py

# from openai import AzureOpenAI
# import os

# client = AzureOpenAI(
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_URL"),
#     api_key=os.getenv("AZURE_OPENAI_API_KEY_COM"),
#     api_version=os.getenv("AZURE_OPENAI_API_VERSION_PRE", "2025-03-01-preview")
# )

# assistant = client.beta.assistants.create(
#     name="Chat Assistant",
#     instructions="You are a helpful assistant.",
#     tools=[
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_products",
#                 "description": "Fetches all product details from the product API",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {},
#                     "required": []
#                 }
#             }
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "update_user",
#                 "description": "Simulates updating a user's details like name, address, phone, etc.",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "user_id": {
#                             "type": "string",
#                             "description": "ID of the user to update"
#                         },
#                         "updates": {
#                             "type": "object",
#                             "description": "Fields to update",
#                             "additionalProperties": True
#                         }
#                     },
#                     "required": ["user_id", "updates"]
#                 }
#             }
#         }
#     ]
# )

# print(" Assistant created! ID:", assistant.id)
# exit()
= - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

assistant = client.beta.assistants.create(
    name="Chat Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "fetch_data",
                "description": "Performs an HTTP request to update user data via a REST API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user to update"
                        },
                        "updates": {
                            "type": "object",
                            "description": "Fields to update for the user (e.g., name, address, phone)",
                            "additionalProperties": True
                        }
                    },
                    "required": ["user_id", "updates"]
                }
            }
        }
    ]
)

# need to change the user 1 details username as emi and phone number as 900807605