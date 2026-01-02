import requests

def test_login(username, password):
    print(f"\n🔍 Testing: {username}")
    
    # Test /token endpoint
    try:
        resp = requests.post(
            "http://localhost:8000/token",
            data={"username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ /token SUCCESS! Role: {data['user']['role']}")
            return True
        else:
            print(f"❌ /token FAILED: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        return False

# Test all users
users = [
    ("admin", "admin123"),
    ("bora_malaj", "admin123"),
    ("gerta_tirana", "admin123"),
    ("arsjana_shehaj", "admin123")
]

print("="*50)
print("FINAL AUTHENTICATION TEST")
print("="*50)

all_pass = True
for user, pwd in users:
    if not test_login(user, pwd):
        all_pass = False

print("\n" + "="*50)
if all_pass:
    print("🎉 ALL TESTS PASSED! Backend authentication is working!")
    print("Now test the frontend in Backend Mode.")
else:
    print("⚠️ Some tests failed. Check database passwords.")