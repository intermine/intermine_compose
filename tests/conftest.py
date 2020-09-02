"""Package-wide test fixtures."""

from typing import Any, Dict, Generator

from _pytest.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from playhouse.postgres_ext import PostgresqlExtDatabase
import pytest

from intermine_compose.app import create_app
from intermine_compose.database import create_db, destroy_test_db, reset_test_db
from intermine_compose.extentions import settings
from intermine_compose.models.actor import Actor
from .factories import ActorFactory


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
    config.addinivalue_line("filterwarnings", "ignore::pytest.PytestCollectionWarning")


@pytest.fixture(scope="class")
def app() -> Generator[FastAPI, None, None]:
    """Create application for the tests."""
    _app = create_app()

    yield _app


@pytest.fixture(scope="class")
def testclient(app: FastAPI) -> TestClient:
    """Create Webtest app."""
    return TestClient(app)


@pytest.fixture(scope="class")
def db(app: FastAPI) -> PostgresqlExtDatabase:
    """Create database for the tests."""
    _db = create_db(settings)
    reset_test_db(_db)

    yield _db

    destroy_test_db(_db)


@pytest.fixture(scope="class")
def user(db: PostgresqlExtDatabase) -> Actor:
    """Create user for the tests."""
    password = "myprecious"  # noqa
    user = ActorFactory(name="bruce", email="bruce@wayne.com", password=password)
    db.session.commit()
    return user


@pytest.fixture(scope="class")
def cookies(user: Actor, testclient: TestClient) -> Dict[Any, Any]:
    """Creates a login cookie."""
    password = "myprecious"  # noqa
    testclient.post_json(
        url="/v1/auth/login/",
        params={"email": user.email, "password": password},
        extra_environ={"wsgi.url_scheme": "https"},
        status="*",
    )
    return testclient.cookies
