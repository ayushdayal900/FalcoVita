def test_metrics_endpoint(client):
    # 1. Trigger some requests first to populate metrics
    client.get("/")
    client.get("/api/doctors/")  # Returns 401, but still registered in metrics
    
    # 2. Fetch metrics
    response = client.get("/metrics")
    assert response.status_code == 200
    
    data = response.data.decode("utf-8")
    # Verify that our custom Prometheus metrics exist in the output
    assert "falcovita_http_requests_total" in data
    assert "falcovita_http_request_duration_seconds" in data
