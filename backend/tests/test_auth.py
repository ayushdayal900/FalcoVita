import json

def test_login_success(client):
    # Verify that a seeded user (e.g. doctor) can log in successfully
    payload = {
        "email": "doctor@test.com",
        "password": "password"
    }
    response = client.post("/api/auth/login", 
                           data=json.dumps(payload),
                           content_type="application/json")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"
    assert data["email"] == "doctor@test.com"
    assert data["role"] == "doctor"
    assert "token" in data


def test_login_invalid_credentials(client):
    # Verify login fails with wrong password
    payload = {
        "email": "doctor@test.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", 
                           data=json.dumps(payload),
                           content_type="application/json")
    
    assert response.status_code == 401
    data = response.get_json()
    assert "Invalid credentials" in data["message"]


def test_register_patient_success(client):
    # Verify registering a patient succeeds
    payload = {
        "name": "New Patient",
        "email": "newpatient@test.com",
        "password": "newpassword123",
        "contact_number": "1122334455",
        "role": "patient",
        "dob": "1995-10-15T00:00:00",
        "contact": "9998887776"
    }
    response = client.post("/api/auth/register", 
                           data=json.dumps(payload),
                           content_type="application/json")
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert data["email"] == "newpatient@test.com"
    assert data["role"] == "patient"


def test_register_duplicate_email(client):
    # Verify registering with an existing email fails
    payload = {
        "name": "Another Patient",
        "email": "doctor@test.com",  # Already exists
        "password": "password",
        "role": "patient",
        "dob": "1995-10-15T00:00:00",
        "contact": "9998887775"
    }
    response = client.post("/api/auth/register", 
                           data=json.dumps(payload),
                           content_type="application/json")
    
    assert response.status_code == 409
    data = response.get_json()
    assert "already exists" in data["message"]
