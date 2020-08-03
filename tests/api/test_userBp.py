from flask_sqlalchemy import SQLAlchemy
from unittest import TestCase
from webtest import TestApp, TestResponse

from intermine_compose.models.users import User


class TestUserAPI:
    """Register a user."""

    def test_can_register(
        self: "TestUserAPI", testapp: TestApp, db: SQLAlchemy
    ) -> None:
        """Register a new user."""
        old_count = len(User.query.all())

        # Post User details to user endpoint
        # for _ in range(0, 10):
        #     params = RegisterSchemaObjFactory()
        #     res: TestResponse = testapp.post_json(
        #         url="/v1/user/", params=params, status="*",
        #     )
        params = {
            "email": "john@doe.me",
            "password": "superpass",
            "firstName": "John",
            "lastName": "Doe",
            "organisation": "InterMine",
        }
        res: TestResponse = testapp.post_json(
            url="/api/v1/user/register", params=params, status="*"
        )
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1


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
