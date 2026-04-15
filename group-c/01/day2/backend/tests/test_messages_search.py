def test_search_valid(client, seeded_db):
    resp = client.get("/api/v1/research/messages/search?q=test")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "items" in data
    assert "nextCursor" in data
    assert "hasMore" in data


def test_search_empty_query(client, seeded_db):
    resp = client.get("/api/v1/research/messages/search?q=")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"]["code"] == "M1_VALIDATION_ERROR"


def test_search_no_query(client, seeded_db):
    resp = client.get("/api/v1/research/messages/search")
    assert resp.status_code == 400


def test_search_has_highlight(client, seeded_db):
    resp = client.get("/api/v1/research/messages/search?q=keywords")
    assert resp.status_code == 200
    data = resp.get_json()
    for item in data["items"]:
        if "highlight" in item and item["highlight"]:
            assert "keywords" in item["highlight"].lower() or "<em>" in item["highlight"]


def test_search_query_too_long(client, seeded_db):
    long_q = "a" * 201
    resp = client.get(f"/api/v1/research/messages/search?q={long_q}")
    assert resp.status_code == 400


def test_search_invalid_date(client, seeded_db):
    resp = client.get("/api/v1/research/messages/search?q=test&from=not-a-date")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"]["code"] == "M1_VALIDATION_ERROR"


def test_search_rate_limit(client, app, seeded_db):
    app.config["RATE_LIMIT_SEARCH_MAX"] = 3
    for i in range(4):
        resp = client.get("/api/v1/research/messages/search?q=test")
    assert resp.status_code == 429
    data = resp.get_json()
    assert data["error"]["code"] == "M1_RATE_LIMIT"
