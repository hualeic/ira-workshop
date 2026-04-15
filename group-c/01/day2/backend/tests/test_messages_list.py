def test_list_default(client, seeded_db):
    resp = client.get("/api/v1/research/messages")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "items" in data
    assert "nextCursor" in data
    assert "hasMore" in data
    assert len(data["items"]) <= 20
    # Verify descending order
    dates = [item["publishedAt"] for item in data["items"]]
    assert dates == sorted(dates, reverse=True)


def test_list_custom_limit(client, seeded_db):
    resp = client.get("/api/v1/research/messages?limit=5")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["items"]) == 5
    assert data["hasMore"] is True
    assert data["nextCursor"] is not None


def test_list_pagination(client, seeded_db):
    resp1 = client.get("/api/v1/research/messages?limit=5")
    data1 = resp1.get_json()
    cursor = data1["nextCursor"]

    resp2 = client.get(f"/api/v1/research/messages?limit=5&cursor={cursor}")
    data2 = resp2.get_json()

    ids1 = {item["messageId"] for item in data1["items"]}
    ids2 = {item["messageId"] for item in data2["items"]}
    assert ids1.isdisjoint(ids2), "No duplicates across pages"


def test_list_invalid_limit(client, seeded_db):
    resp = client.get("/api/v1/research/messages?limit=200")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"]["code"] == "M1_VALIDATION_ERROR"


def test_list_unread_only(client, seeded_db):
    resp = client.get("/api/v1/research/messages?unreadOnly=true")
    assert resp.status_code == 200
    data = resp.get_json()
    for item in data["items"]:
        assert item["read"] is False


def test_list_category_filter(client, seeded_db):
    resp = client.get("/api/v1/research/messages?category=宏观经济")
    assert resp.status_code == 200
    data = resp.get_json()
    for item in data["items"]:
        assert item["category"] == "宏观经济"


def test_list_has_read_field(client, seeded_db):
    resp = client.get("/api/v1/research/messages")
    data = resp.get_json()
    for item in data["items"]:
        assert "read" in item
        assert isinstance(item["read"], bool)


def test_list_fields_match_dto(client, seeded_db):
    resp = client.get("/api/v1/research/messages?limit=1")
    data = resp.get_json()
    item = data["items"][0]
    required_fields = {"messageId", "title", "summary", "publishedAt", "read"}
    assert required_fields.issubset(item.keys())
