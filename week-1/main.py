import os
import json
import urllib.request
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

# Using the correct model name from your key's available list
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"

# Request Payload
payload = {
    "contents": [{
        "parts": [{
            "text": "What is Artificial Intelligence? Explain in simple words."
        }]
    }]
}

headers = {'Content-Type': 'application/json'}

# Make the request using built-in urllib
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        answer = result['candidates'][0]['content']['parts'][0]['text']
        print("\nLLM Response:")
        print(answer)
except Exception as e:
    print(f"Error: {e}")
