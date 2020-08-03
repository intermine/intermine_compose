"""Package-wide test fixtures."""

from typing import Any, Dict, Generator
import os


from environs import Env
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
from _pytest.config import Config
from webtest import TestApp

from intermine_compose.app import create_app
from intermine_compose.config import Config as AppConfig
from intermine_compose.extentions import db as _db

collect_ignore_classes = [TestApp]


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
def db(app: Flask) -> SQLAlchemy:
    """Create database for the tests."""
    _db.init_app(app)
    with app.app_context():
        _db.drop_all()
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope="class")
def testapp(app: Flask, db: SQLAlchemy) -> TestApp:
    """Create Webtest app."""
    return TestApp(app)


# @pytest.fixture(scope="module")
# def cookies(client):
#     """
#     This fixture will be used to generate cookies for using in requests where authentication is required.
#     """

#     resp = client.post(
#         "/api/v1/user/register",
#         json={
#             "email": "test@user.me",
# 	        "password": "superpass",
# 	        "firstName": "Bruce",
# 	        "lastName": "Stark",
# 	        "organisation": "InterMine"
#         }
#     )
#     assert resp.status_code == 200
#     resp = client.post(
#         "/api/v1/user/login",
#         json={
#             "email": "test@user.me",
#             "password": "superpass"
#         }
#     )
#     assert resp.status_code == 200
#     cookies = resp.headers['Set-Cookie']
#     return cookies
