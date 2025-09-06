{
  "name": "update_user",
  "description": "Simulates updating a user's details like name, address, phone, etc.",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "ID of the user to update"
      },
      "updates": {
        "type": "object",
        "description": "Fields to update for the user (e.g., last_name, phone)",
        "additionalProperties": true
      }
    },
    "required": ["user_id", "updates"]
  },
  "metrics": {
    "url": "/users/{user_id}",
    "method": "PUT",
    "description": "Updates user details"
  }
}
