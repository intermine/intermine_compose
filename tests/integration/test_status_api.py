"""Status API test."""

from webtest import TestApp, TestResponse


def test_status(testapp: TestApp) -> None:
    """Test status get."""
    resp: TestResponse = testapp.get(url="/api/v1/status/")
    assert resp.status_code == 200
