Here is the Python code to consume the provided APIs:

```python
import requests

# Replace with your actual API key and external user ID
API_KEY = "<replace_api_key>"
EXTERNAL_USER_ID = "<replace_external_user_id>"

# Base URL for the APIs
BASE_URL = "https://api-dev.on-demand.io/chat/v1"

def create_chat_session():
    """
    Create a chat session and return the session ID.
    """
    url = f"{BASE_URL}/sessions"
    headers = {
        "apikey": API_KEY
    }
    body = {
        "pluginIds": [],
        "externalUserId": EXTERNAL_USER_ID
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 201:
        session_id = response.json().get("data", {}).get("id")
        if session_id:
            return session_id
        else:
            raise ValueError("Session ID not found in the response.")
    else:
        raise Exception(f"Failed to create chat session. Status Code: {response.status_code}, Response: {response.text}")

def submit_query(session_id, query, response_mode="sync"):
    """
    Submit a query to the chat session.
    """
    url = f"{BASE_URL}/sessions/{session_id}/query"
    headers = {
        "apikey": API_KEY
    }
    body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": query,
        "pluginIds": [
            "plugin-1712327325", "plugin-1713962163", "plugin-1716164040",
            "plugin-1722504304", "plugin-1713954536", "plugin-1713958591",
            "plugin-1713958830", "plugin-1713961903", "plugin-1713967141"
        ],
        "responseMode": response_mode,
        "reasoningMode": "medium"
    }

    if response_mode == "sync":
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to submit query. Status Code: {response.status_code}, Response: {response.text}")
    elif response_mode == "stream":
        # Handle Server-Sent Events (SSE) using requests
        with requests.post(url, headers=headers, json=body, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        print(line.decode('utf-8'))
            else:
                raise Exception(f"Failed to submit query in stream mode. Status Code: {response.status_code}, Response: {response.text}")
    else:
        raise ValueError("Invalid response mode. Use 'sync' or 'stream'.")

if __name__ == "__main__":
    try:
        # Step 1: Create a chat session
        session_id = create_chat_session()
        print(f"Chat session created with ID: {session_id}")

        # Step 2: Submit a query in sync mode
        query = "Put your query here"
        response = submit_query(session_id, query, response_mode="sync")
        print("Sync Response:", response)

        # Step 3: Submit a query in stream mode (optional)
        print("Stream Response:")
        submit_query(session_id, query, response_mode="stream")

    except Exception as e:
        print(f"Error: {e}")
