"""Package-wide test fixtures."""

from typing import Any, Dict, Generator

from _pytest.config import Config
from environs import Env
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
from webtest import TestApp

from intermine_compose.app import create_app
from intermine_compose.config import Config as AppConfig
from intermine_compose.extentions import db as _db
from intermine_compose.models.actor import Actor
from .factories import ActorFactory


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
    config.addinivalue_line("filterwarnings", "ignore::pytest.PytestCollectionWarning")


@pytest.fixture(scope="class")
def app() -> Generator[Flask, None, None]:
    """Create application for the tests."""
    env = Env()
    env.read_env()
    if env.bool("CI", default=False):
        _app = create_app(AppConfig.CI)
    else:
        _app = create_app(AppConfig.TEST)
    ctx = _app.test_request_context()
    ctx.push()  # type: ignore

    yield _app

    ctx.pop()  # type: ignore


@pytest.fixture(scope="class")
def testapp(app: Flask, db: SQLAlchemy) -> TestApp:
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture(scope="class")
def db(app: Flask) -> SQLAlchemy:
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.drop_all()
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope="class")
def user(db: SQLAlchemy) -> Actor:
    """Create user for the tests."""
    password = "myprecious"  # noqa
    user = ActorFactory(name="bruce", email="bruce@wayne.com", password=password)
    db.session.commit()
    return user


@pytest.fixture(scope="class")
def cookies(user: Actor, testapp: TestApp) -> Dict[Any, Any]:
    """Creates a login cookie."""
    password = "myprecious"  # noqa
    testapp.post_json(
        url="/v1/auth/login/",
        params={"email": user.email, "password": password},
        extra_environ={"wsgi.url_scheme": "https"},
        status="*",
    )
    return testapp.cookies
