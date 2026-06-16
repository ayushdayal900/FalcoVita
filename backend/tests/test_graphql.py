import json

def test_graphql_query_doctors(client):
    query = """
    query {
      doctors {
        id
        specialization
        user {
          name
          email
        }
      }
    }
    """
    response = client.post("/graphql", 
                           data=json.dumps({"query": query}), 
                           content_type="application/json")
    
    assert response.status_code == 200
    res_data = response.get_json()
    assert "errors" not in res_data
    assert "data" in res_data
    doctors = res_data["data"]["doctors"]
    assert len(doctors) >= 1
    assert doctors[0]["specialization"] == "Cardiology"
    assert doctors[0]["user"]["email"] == "doctor@test.com"


def test_graphql_appointment_lifecycle(client):
    # 1. Fetch doctor, patient, and department IDs first dynamically
    query_ids = """
    query {
      doctors {
        id
        department {
          id
        }
      }
      patients {
        id
      }
    }
    """
    response = client.post("/graphql", 
                           data=json.dumps({"query": query_ids}), 
                           content_type="application/json")
    
    assert response.status_code == 200
    data = response.get_json()["data"]
    doctor_id = data["doctors"][0]["id"]
    department_id = data["doctors"][0]["department"]["id"]
    patient_id = data["patients"][0]["id"]

    # 2. Run createAppointment mutation
    mutation_create = f"""
    mutation {{
      createAppointment(
        patientId: {patient_id},
        doctorId: {doctor_id},
        departmentId: {department_id},
        appointmentDate: "2026-07-20T10:00:00Z"
      ) {{
        success
        appointment {{
          id
          status
          appointmentDate
        }}
      }}
    }}
    """
    response = client.post("/graphql", 
                           data=json.dumps({"query": mutation_create}), 
                           content_type="application/json")
    assert response.status_code == 200
    res_create = response.get_json()
    assert "errors" not in res_create
    assert res_create["data"]["createAppointment"]["success"] is True
    appt_id = res_create["data"]["createAppointment"]["appointment"]["id"]
    assert res_create["data"]["createAppointment"]["appointment"]["status"] == "scheduled"

    # 3. Run updateAppointmentStatus mutation
    mutation_update = f"""
    mutation {{
      updateAppointmentStatus(id: {appt_id}, status: "completed") {{
        success
        appointment {{
          id
          status
        }}
      }}
    }}
    """
    response = client.post("/graphql", 
                           data=json.dumps({"query": mutation_update}), 
                           content_type="application/json")
    assert response.status_code == 200
    res_update = response.get_json()
    assert "errors" not in res_update
    assert res_update["data"]["updateAppointmentStatus"]["success"] is True
    assert res_update["data"]["updateAppointmentStatus"]["appointment"]["status"] == "completed"
