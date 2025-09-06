{
  "messages": [
    {
      "role": "user",
      "content": "Hi, show me the available products."
    }
  ],
  "action_details": {
    "url": "https://example.com/api/search",
    "description": "Search products",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer token",
      "Content-Type": "application/json"
    },
    "content_type": "application/json",
    "input": [
      {
        "query": "laptop",
        "max_results": 5
      }
    ]
  }
}


{
  "thread_id": null,
  "messages": [
    {
      "role": "user",
      "content": "Show me some products"
    }
  ],
  "action_details": {
    "url": "https://fakestoreapi.com/products",
    "description": "Fetch list of available products from the fake store API",
    "method": "GET",
    "headers": {
      "Content-Type": "application/json"
    },
    "content_type": "application/json",
    "input": []
  }
}

{
"messages": [
    {
      "role": "user",
      "content": "Hi, show me the available products."
    }
  ],
"action_details": {   
    "url": "https://fakestoreapi.com/products",
    "description": "Fetch list of available products from the fake store API",
    "method": "GET",
    "headers": {
      "Content-Type": "application/json" 
    },
    "content_type": "application/json",
    "input": []
  }
}