def test_status(client):
    resp = client.get(
        "/api/v1/status/"
    )
    assert resp.status_code == 200