def test_list_tenants_empty(client):
    r = client.get("/tenants")
    assert r.status_code == 200
    body = r.json()
    assert body["items"] == []
    assert body["total"] == 0
