import requests
import json

url = "http://127.0.0.1:8000/predict"

with open("dummy_data.json", "r") as f:
    data = json.load(f)

response = requests.post(url, json=data)

print(response.json())