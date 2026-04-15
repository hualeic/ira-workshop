def test_health(client):
    resp = client.get("/api/v1/research/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert data["module"] == "M1"
    assert data["version"] == "1.0.0"
