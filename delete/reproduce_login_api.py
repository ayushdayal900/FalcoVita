import requests

def test_login():
    url = "http://localhost:5000/api/auth/login"
    payload = {
        "email": "doctor1@hospital.com",
        "password": "Doctor@123"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
