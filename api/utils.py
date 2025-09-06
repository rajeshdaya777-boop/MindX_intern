import requests
from fastapi import HTTPException
from typing import Optional, Dict

def fetch_data(method: str, base_url: str, endpoint: str, json_payload: Optional[Dict] = None):
    url = base_url + endpoint
    headers = {"Content-Type": "application/json"}
    print(f"Making {method} request to: {url} with payload: {json_payload}")

    try:
        response = requests.request(method.upper(), url, headers=headers, json=json_payload)
        response.raise_for_status()
        print(f"Response Status: {response.status_code}, Response Content: {response.text}")
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
