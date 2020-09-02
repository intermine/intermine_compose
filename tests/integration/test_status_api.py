"""Status API test."""

from fastapi.testclient import TestClient


def test_status(testclient: TestClient) -> None:
    """Test status get."""
    resp = testclient.get(url="/v1/status/")
    assert resp.status_code == 200
