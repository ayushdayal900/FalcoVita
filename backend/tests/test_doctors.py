import json
from backend.services import DoctorService

def test_get_all_doctors_service(app):
    with app.app_context():
        doctors = DoctorService.get_all()
        assert len(doctors) >= 1
        assert doctors[0]["specialization"] == "Cardiology"


def test_doctor_rest_endpoints(client, app):
    # 1. Log in as admin to get auth token
    payload = {
        "email": "admin@test.com",
        "password": "password"
    }
    login_resp = client.post("/api/auth/login", 
                             data=json.dumps(payload), 
                             content_type="application/json")
    assert login_resp.status_code == 200
    token = login_resp.get_json()["token"]
    headers = {
        "Authentication-Token": token
    }

    # 2. Get list of doctors via REST
    get_resp = client.get("/api/doctors/", headers=headers)
    assert get_resp.status_code == 200
    doctors_list = get_resp.get_json()
    assert len(doctors_list) >= 1
    doctor_id = doctors_list[0]["id"]

    # 3. Get specific doctor detail
    detail_resp = client.get(f"/api/doctors/{doctor_id}", headers=headers)
    assert detail_resp.status_code == 200
    doctor_detail = detail_resp.get_json()
    assert doctor_detail["specialization"] == "Cardiology"

    # 4. Update doctor experience
    update_payload = {
        "specialization": "Cardiology",
        "qualifications": "MBBS, MD",
        "experience": 12  # Updated from 10
    }
    put_resp = client.put(f"/api/doctors/{doctor_id}", 
                          data=json.dumps(update_payload),
                          content_type="application/json",
                          headers=headers)
    assert put_resp.status_code == 200
    assert put_resp.get_json()["experience"] == 12


def test_search_doctors_endpoint(client):
    payload = {
        "email": "admin@test.com",
        "password": "password"
    }
    login_resp = client.post("/api/auth/login", 
                             data=json.dumps(payload), 
                             content_type="application/json")
    token = login_resp.get_json()["token"]
    headers = {"Authentication-Token": token}

    # Query search endpoint (DB fallback test since OpenSearch is off during tests)
    search_resp = client.get("/api/search/doctors?q=Test", headers=headers)
    assert search_resp.status_code == 200
    results = search_resp.get_json()
    assert len(results) >= 1
    assert "Cardiology" in results[0]["specialization"]
