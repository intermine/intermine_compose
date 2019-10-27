import pytest
import intermine_compose
import os

@pytest.fixture(scope="session")
def client():
    """
    This fixture will create an app instance, setup test db connection and create all tables.
    At the end of tests, connection to test db is closed and all tables are dropped.
    This app instance and db connection is used for the entire test.
    """
    os.environ.putenv("FLASK_CONFIG_MODE", "testing")
    app = intermine_compose.create_app()
    app.app_context().push()
    client = app.test_client()
    yield client

@pytest.fixture(scope="module")
def cookies(client):
    """
    This fixture will be used to generate cookies for using in requests where authentication is required.
    """

    resp = client.post(
        "/api/v1/user/register",
        json={
            "email": "test@user.me",
	        "password": "superpass",
	        "firstName": "Bruce",
	        "lastName": "Stark",
	        "organisation": "InterMine"
        }
    )
    assert resp.status_code == 200
    resp = client.post(
        "/api/v1/user/login",
        json={
            "email": "test@user.me",
            "password": "superpass"
        }
    )
    assert resp.status_code == 200
    cookies = resp.headers['Set-Cookie']
    return cookies
