def test_detail_valid(client, seeded_db):
    msg_id = seeded_db[0].id
    resp = client.get(f"/api/v1/research/messages/{msg_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["messageId"] == msg_id
    assert "body" in data
    assert "contentFormat" in data
    assert "links" in data
    assert "metadata" in data
    assert "read" in data


def test_detail_not_found(client, seeded_db):
    fake_id = "00000000-0000-0000-0000-000000000099"
    resp = client.get(f"/api/v1/research/messages/{fake_id}")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"]["code"] == "M1_MESSAGE_NOT_FOUND"


def test_detail_has_trace_id(client, seeded_db):
    fake_id = "00000000-0000-0000-0000-000000000099"
    resp = client.get(f"/api/v1/research/messages/{fake_id}")
    data = resp.get_json()
    assert "traceId" in data["error"]
    assert data["error"]["traceId"].startswith("trace_")
