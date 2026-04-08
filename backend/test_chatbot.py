import urllib.request
import json
import urllib.error

url = 'http://localhost:5005/api/chatbot'
data = json.dumps({"query": "Analyze", "drugs": ["warfarin", "aspirin"], "interaction": {"severity": "severe", "mechanism": "testing"}}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except urllib.error.HTTPError as e:
    print("Error Code:", e.code)
    print("Error Body:", e.read().decode())
