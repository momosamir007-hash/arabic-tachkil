import requests
import json

url = "http://127.0.0.1:8000/api/v1/process"
payload = {
    "action": "stanza",
    "text": "زار الملك القاهرة."
}

def log(msg):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

log("Final API Stanza Test...")
try:
    response = requests.post(url, json=payload)
    log(f"Status: {response.status_code}")
    log(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    log(f"Error: {e}")
