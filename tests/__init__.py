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
    client = app.test_client()
    yield client
    intermine_compose.models.drop_all_tables()
