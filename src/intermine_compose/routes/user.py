"""User API."""

from http import HTTPStatus
from typing import Optional, Union

from flask import Blueprint, current_app, jsonify, make_response, request, Response
from flask_login import login_required, login_user, logout_user
from flask_login.utils import current_user
from marshmallow import ValidationError

from intermine_compose.database import db
from intermine_compose.extentions import login_manager
from intermine_compose.models.actor import Actor
from intermine_compose.routes.user_schema import (
    ResetPassword,
    ResetPasswordRequest,
    UserLogin,
    UserRegister,
)

user_bp = Blueprint("users", __name__, url_prefix="/api/v1/user")


@login_manager.user_loader
def load_user(user_id: Union[int, str]) -> Optional[Actor]:
    """Load user by ID."""
    return Actor.get_by_id(int(user_id))


@user_bp.route("/register", methods=["POST"])
def register() -> Response:
    """Register user."""
    # return early if user is already logged in
    if current_user.is_authenticated:
        return make_response(
            jsonify({"message": "User is already authenticated"}), HTTPStatus.OK
        )

    # validate user input
    try:
        form = UserRegister().load(request.json)
    except ValidationError as errors:
        response = make_response(jsonify(str(errors)), HTTPStatus.BAD_REQUEST)
        return response

    # Create user if checks are passed
    try:
        _ = Actor.create(**form)
        db.session.remove()
    except BaseException:
        return make_response(
            jsonify({"message": "DATABASE ERROR"}), HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return make_response(jsonify({"message": "User is created"}), HTTPStatus.OK)


@user_bp.route("/login", methods=["POST"])
def login() -> Response:
    """Auth api to login user."""
    # return early if user is already logged in
    if current_user.is_authenticated:
        return make_response(
            jsonify({"message": "User is already authenticated"}), HTTPStatus.OK
        )

    # validate user input
    try:
        form = UserLogin().load(request.json)
    except ValidationError as errors:
        response = make_response(jsonify(str(errors)), HTTPStatus.BAD_REQUEST)
        return response

    # query db to verify if user with given email exists
    try:
        user: Actor = Actor.query.filter_by(email=form["email"]).first()
    except BaseException:
        return make_response(
            jsonify({"message": "DATABASE ERROR"}), HTTPStatus.INTERNAL_SERVER_ERROR
        )

    # return error if user not exist
    if not user:
        db.session.remove()
        return make_response(
            jsonify({"message": "unknown user or invalid password"}),
            HTTPStatus.BAD_REQUEST,
        )

    pass_match = user.check_password(form["password"])

    # return error if password match failed
    if not pass_match:
        return make_response(
            jsonify({"message": "unknown user or invalid password"}),
            HTTPStatus.BAD_REQUEST,
        )

    # login user after checks
    login_user(user)
    return make_response(jsonify({"message": "Successfully logged in"}), HTTPStatus.OK)


@user_bp.route("/logout", methods=["GET"])
@login_required
def logout() -> Response:
    """Logout."""
    logout_user()
    return make_response(jsonify({"message": "Successfully logged out"}), HTTPStatus.OK)


# @user_bp.route("/profile", methods=["GET"])
# @login_required
# def profile():
#     slim_user_schema_instance = SlimUserSchema()
#     user_profile_schema_instance = UserProfileSchema()
#     if request.method == "GET":
#         profile = slim_user_schema_instance.dump(
#             User.query.filter_by(id=current_user.get_id()).first()
#         )
#         return jsonify(profile.data)
#     else:
#         errors = user_profile_schema_instance.validate(request.json)
#         if errors:
#             response = make_response(jsonify(errors), HTTPStatus.BAD_REQUEST)
#             return response
#         user_profile_schema_instance = user_profile_schema_instance.load(request.json)
#         user = User.query.filter_by(id=current_user.get_id())
#         user.update(user_profile_schema_instance.data)
#         try:
#             db.session.commit()
#             return jsonify({"message": "Profile successfully updated"})
#         except:
#             abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO UPDATE USER"))


# @user_bp.route("/forgotpassword", methods=["POST"])
# def get_reset_password() -> Response:
#     """Request password reset."""
#     # validate user input
#     try:
#         form = ResetPasswordRequest().load(request.json)
#     except ValidationError as errors:
#         response = make_response(jsonify(str(errors)), HTTPStatus.BAD_REQUEST)
#         return response

#     # query db to verify if user with given email exists
#     try:
#         user: Actor = Actor.query.filter_by(email=form["email"]).first()
#     except BaseException:
#         return make_response(
#             jsonify({"message": "DATABASE ERROR"}), HTTPStatus.INTERNAL_SERVER_ERROR
#         )

#     # return error if user not exist
#     if user:
#         try:
#             sendResetPasswordMail(current_app, user)
#         except BaseException:
#             # ignore email send errors
#             pass
#     return make_response(
#         jsonify({"message": "Password reset request accepted"}), HTTPStatus.OK
#     )


# @user_bp.route("/resetpassword", methods=["POST"])
# def post_reset_password() -> Response:
#     """Password reset."""
#     # validate user input
#     try:
#         form = ResetPassword().load(request.json)
#     except ValidationError as errors:
#         response = make_response(jsonify(str(errors)), HTTPStatus.BAD_REQUEST)
#         return response

#     # validate token
#     try:
#         user = Actor.verify_reset_password_token(form["token"])
#     except DecodeError:
#         return make_response(jsonify({"message": "Bad token"}), HTTPStatus.BAD_REQUEST)
#     except BaseException:
#         return make_response(
#             jsonify({"message": "DATABASE ERROR"}), HTTPStatus.INTERNAL_SERVER_ERROR
#         )

#     if user:
#         return make_response(
#             jsonify({"message": "Password reset successfull"}), HTTPStatus.OK
#         )

#     return make_response(jsonify({"message": "Bad token"}), HTTPStatus.BAD_REQUEST)
