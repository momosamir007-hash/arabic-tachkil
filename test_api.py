import requests
import json

url = "http://127.0.0.1:8000/api/v1/process"
payload = {
    "action": "sentiment",
    "text": "هذا مشروع رائع جداً!"
}

try:
    print(f"Testing {payload['action']}...")
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")

payload["action"] = "stanza"
payload["text"] = "زار الملك القاهرة."
try:
    print(f"\nTesting {payload['action']}...")
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
