"""Tests for User API."""

# from flask_sqlalchemy import SQLAlchemy
import pytest
from webtest import TestApp, TestResponse

from intermine_compose.models.actor import Actor
from ..factories import ActorFactory, RegisterSchemaObjFactory


@pytest.mark.usefixtures("db")
class TestUserApi:
    """User API tests."""

    def test_can_register(self: "TestUserApi", testapp: TestApp) -> None:
        """Register a new user."""
        old_count = len(Actor.query.all())

        # Post User details to user endpoint
        for _ in range(0, 10):
            params = RegisterSchemaObjFactory()
            res: TestResponse = testapp.post_json(
                url="/api/v1/user/register", params=params, status="*",
            )

            assert res.status_code == 200
        # new users created
        assert len(Actor.query.all()) == old_count + 10

    def test_sees_error_message_if_user_already_registered(
        self: "TestUserApi", user: Actor, testapp: TestApp
    ) -> None:
        """Show error if user already registered."""
        user = ActorFactory(active=True)  # A registered user
        user.save()

        # Post User details to user endpoint
        res: TestResponse = testapp.post_json(
            url="/api/v1/user/register",
            params={
                "name": "Bruce Wayne",
                "email": user.email,
                "organisation": "Wayne Enterprises",
                "password": "iAMBetterThanStark",
            },
            status="*",
        )
        # sees error
        assert "email is already present" in str(res.json)


# def test_register(client):
#     resp = client.post(
#         "/api/v1/user/register",
#         json={
#             "email": "john@doe.me",
# 	        "password": "superpass",
# 	        "firstName": "John",
# 	        "lastName": "Doe",
# 	        "organisation": "InterMine"
#         }
#     )
#     assert resp.status_code == 200

# def test_login(client):
#     resp = client.post(
#         "/api/v1/user/login",
#         json={
#             "email": "john@doe.me",
#             "password": "superpass"
#         }
#     )
#     assert resp.status_code == 200

# def test_get_profile(client):
#     resp = client.get(
#         "api/v1/user/profile"
#     )
#     assert resp.status_code == 200
#     assert resp.get_json() == {
#         "email": "john@doe.me",
# 	    "firstName": "John",
# 	    "lastName": "Doe",
# 	    "organisation": "InterMine"
#     }

# def test_update_profile(client):
#     resp = client.post(
#         "api/v1/user/profile",
#         json={
# 	        "firstName": "JohnNew",
# 	        "lastName": "DoeNew",
# 	        "organisation": "InterMineNew"
#         }
#     )
#     assert resp.status_code == 200
#     resp = client.get(
#         "api/v1/user/profile"
#     )
#     assert resp.status_code == 200
#     assert resp.get_json() == {
#         "email": "john@doe.me",
# 	    "firstName": "JohnNew",
# 	    "lastName": "DoeNew",
# 	    "organisation": "InterMineNew"
#     }


# def test_logout(client):
#     resp = client.get(
#         "api/v1/user/logout"
#     )
#     assert resp.status_code == 200
