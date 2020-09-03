"""Package-wide test fixtures."""

from typing import Dict, Generator

from _pytest.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from playhouse.postgres_ext import PostgresqlExtDatabase
import pytest
from requests.cookies import RequestsCookieJar

from intermine_compose.app import create_app
from intermine_compose.database import create_db, destroy_test_db, reset_test_db
from intermine_compose.extentions import settings
from intermine_compose.models.actor import Actor
from intermine_compose.routes.auth_schemas import AuthLoginSchema
from .factories import ActorFactory


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
    config.addinivalue_line("filterwarnings", "ignore::pytest.PytestCollectionWarning")


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, None, None]:
    """Create application for the tests."""
    _app = create_app()

    yield _app


@pytest.fixture(scope="function")
def testclient(app: FastAPI) -> TestClient:
    """Create Webtest app."""
    return TestClient(app)


@pytest.fixture(scope="session")
def db(app: FastAPI) -> PostgresqlExtDatabase:
    """Create database for the tests."""
    _db = create_db(settings)
    reset_test_db(_db)

    yield _db

    destroy_test_db(_db)


@pytest.fixture(scope="session")
def user(db: PostgresqlExtDatabase) -> Actor:
    """Create user for the tests."""
    password = "myprecious"  # noqa
    user = ActorFactory(name="bruce", email="bruce@wayne.com", password=password)
    return user


@pytest.fixture(scope="session")
def cookie_jar(user: Actor, app: FastAPI) -> Dict:
    """Creates a login cookie."""
    testclient = TestClient(app)
    password = "myprecious"  # noqa
    params = AuthLoginSchema(email=user.email, password=password).dict()
    res = testclient.post(url="/v1/auth/login/", json=params)
    cookie_header = res.headers["set-cookie"]
    assert res.status_code == 200
    assert settings.COOKIE_DOMAIN in cookie_header
    assert settings.APP_NAME in cookie_header
    cookie_dict = {}
    cookie_dict["name"] = cookie_header.split(";")[0].split("=")[0]
    cookie_dict["value"] = cookie_header.split(";")[0].split("=")[1]
    jar = RequestsCookieJar()
    jar.set(cookie_dict["name"], cookie_dict["value"])
    return jar
