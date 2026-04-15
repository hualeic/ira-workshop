def test_mark_read(client, seeded_db):
    msg_id = seeded_db[5].id  # An unread message
    resp = client.patch(f"/api/v1/research/messages/{msg_id}/read")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["messageId"] == msg_id
    assert data["read"] is True
    assert "readAt" in data


def test_mark_read_idempotent(client, seeded_db):
    msg_id = seeded_db[5].id
    resp1 = client.patch(f"/api/v1/research/messages/{msg_id}/read")
    resp2 = client.patch(f"/api/v1/research/messages/{msg_id}/read")
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert resp1.get_json()["read"] == resp2.get_json()["read"] == True


def test_mark_read_not_found(client, seeded_db):
    fake_id = "00000000-0000-0000-0000-000000000099"
    resp = client.patch(f"/api/v1/research/messages/{fake_id}/read")
    assert resp.status_code == 404


def test_mark_read_reflects_in_list(client, seeded_db):
    msg_id = seeded_db[5].id

    resp_before = client.get("/api/v1/research/messages")
    items_before = resp_before.get_json()["items"]
    target_before = next((i for i in items_before if i["messageId"] == msg_id), None)
    if target_before:
        assert target_before["read"] is False

    client.patch(f"/api/v1/research/messages/{msg_id}/read")

    resp_after = client.get("/api/v1/research/messages")
    items_after = resp_after.get_json()["items"]
    target_after = next((i for i in items_after if i["messageId"] == msg_id), None)
    if target_after:
        assert target_after["read"] is True
