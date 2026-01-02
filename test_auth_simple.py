# test_simple.py
import requests
import json

print("Testing SIMPLE login (no bcrypt verification)...")

# Direct test
response = requests.post(
    "http://localhost:8000/token",
    data={"username": "bora_malaj", "password": "admin123"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

if response.status_code == 200:
    print("\n✅ SUCCESS! Copy this token to test in frontend:")
    data = response.json()
    print(f"Token: {data['access_token']}")
    print(f"User role: {data['user']['role']}")