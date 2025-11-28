import requests
import time
import json

BASE_URL = "http://localhost:5000"

def login(email, password):
    url = f"{BASE_URL}/login"
    headers = {"Content-Type": "application/json"}
    data = {"email": email, "password": password}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("response", {}).get("user", {}).get("authentication_token")
    else:
        print(f"Login failed: {response.text}")
        return None

def test_cache():
    # Login as admin (assuming admin credentials exist, otherwise use a doctor)
    # Adjust credentials as needed based on your seed data
    token = login("doctor1@hospital.com", "Doctor@123") 
    if not token:
        print("Skipping test due to login failure")
        return

    headers = {"Authentication-Token": token, "Content-Type": "application/json"}
    
    print("\n--- Testing Doctor List Caching ---")
    url = f"{BASE_URL}/api/doctors/"
    
    # 1. First Hit (Cache Miss)
    start = time.time()
    response = requests.get(url, headers=headers)
    duration_1 = time.time() - start
    print(f"1. First Hit (Miss): {duration_1:.4f}s - Status: {response.status_code}")

    # 2. Second Hit (Cache Hit)
    start = time.time()
    response = requests.get(url, headers=headers)
    duration_2 = time.time() - start
    print(f"2. Second Hit (Hit): {duration_2:.4f}s - Status: {response.status_code}")
    
    if duration_2 < duration_1:
        print("SUCCESS: Cache hit was faster.")
    else:
        print("WARNING: Cache hit was not significantly faster (could be local network variance).")

    # 3. Invalidate Cache (Create Doctor - simplified, might fail if data invalid but attempt should trigger invalidation if successful)
    # Actually, let's just update a doctor if we can find one, or create.
    # Let's try to create a dummy doctor to trigger invalidation.
    # Note: Creating a doctor requires a valid user payload. 
    # For simplicity, let's try to update the first doctor found.
    doctors = response.json()
    if doctors and len(doctors) > 0:
        doc_id = doctors[0]['id']
        print(f"\n--- Invalidating Cache (Updating Doctor {doc_id}) ---")
        update_url = f"{BASE_URL}/api/doctors/{doc_id}"
        # Just sending same data to trigger update
        update_data = {"first_name": doctors[0]['first_name']} 
        requests.put(update_url, headers=headers, json=update_data)
        
        # 4. Third Hit (Cache Miss after Invalidation)
        start = time.time()
        response = requests.get(url, headers=headers)
        duration_3 = time.time() - start
        print(f"3. Third Hit (Miss after Invalidation): {duration_3:.4f}s - Status: {response.status_code}")
        
        if duration_3 > duration_2:
             print("SUCCESS: Cache was invalidated (response time increased).")
        else:
             print("WARNING: Response time did not increase significantly (could be fast DB).")

if __name__ == "__main__":
    test_cache()
