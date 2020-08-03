from webtest import TestApp, TestResponse


def test_status(testapp: TestApp) -> None:
    resp = testapp.get(url="/api/v1/status/")
    assert resp.status_code == 200
