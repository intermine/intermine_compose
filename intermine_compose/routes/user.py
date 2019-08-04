from flask import Blueprint, request, jsonify, abort, make_response
from flask_login import login_required, login_user, logout_user, current_user
from http import HTTPStatus
import sys
import bcrypt

# did relative imports here (Make sure to change this during refactoring )
from ..models.users import UserRegisterSchema, UserCredentialsSchema, SlimUserSchema, UserProfileSchema, User
from ..models import db
from ..auth import login_manager

user_bp = Blueprint("users", __name__, url_prefix="/api/v1/user")

@user_bp.route("/register", methods=["POST"])
def register():
    
    # validate user input
    user_register_schema_instance = UserRegisterSchema()
    errors = user_register_schema_instance.validate(request.json)
    if errors:
        response = make_response(jsonify(errors), HTTPStatus.BAD_REQUEST)
        return response

    # load user registration data into user_register_schema_instance
    # Note: we are re using the variable here!!
    user_register_schema_instance = user_register_schema_instance.load(request.json)

    # query db to verify if email is not already registered
    email_exists = User.query.filter_by(email = user_register_schema_instance.data["email"]).first()
    
    # return error if email already exist
    if email_exists:
        response = make_response(jsonify({"message":"EMAIL ALREADY EXIST"}), HTTPStatus.BAD_REQUEST)
        return response
    
    # hash user password
    user_register_schema_instance.data["password"] = bcrypt.hashpw(
        user_register_schema_instance.data["password"].encode('utf-8'), bcrypt.gensalt()).hex()
    
    # create user object for inserting it into db
    user = User(**user_register_schema_instance.data)
    
    # insert user to db if all checks are ok
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"Successfully registered a new user"}) 
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO REGISTER USER"))
    
@user_bp.route("/login", methods=["POST"])
def login():

    #return early if user is already logged in
    if current_user.is_authenticated:
        return jsonify({"message":"User is already authenticated"})
    
    # validate user input
    user_credentials_schema_instance = UserCredentialsSchema()
    errors = user_credentials_schema_instance.validate(request.json)
    if errors:
        response = make_response(jsonify(errors), HTTPStatus.BAD_REQUEST)
        return response

    # load user credential data into user_credentials_schema_instance
    # Note: we are re using the variable here!!
    user_credentials_schema_instance = user_credentials_schema_instance.load(request.json)

    # query db to verify if user with given email exists
    user = User.query.filter_by(email = user_credentials_schema_instance.data["email"]).first()
    
    # return error if user not exist
    if not user:
        abort(HTTPStatus.BAD_REQUEST)
    
    pass_match = bcrypt.checkpw(user_credentials_schema_instance.data["password"].encode('utf8'), bytes.fromhex(user.password))
    # return error if password match failed
    if not pass_match:
        abort(HTTPStatus.BAD_REQUEST)

    # login user after checks
    login_user(user)

    return jsonify({"message":"Successfully logged in"})

@user_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Successfully logged out user"})
    
@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    slim_user_schema_instance = SlimUserSchema()
    user_profile_schema_instance = UserProfileSchema()
    if request.method == "GET":
        profile = slim_user_schema_instance.dump(
            User.query.filter_by(id=current_user.get_id()).first()
        )
        return jsonify(profile.data)
    else:
        errors = user_profile_schema_instance.validate(request.json)
        if errors:
            response = make_response(jsonify(errors), HTTPStatus.BAD_REQUEST)
            return response
        user_profile_schema_instance = user_profile_schema_instance.load(request.json)
        user = User.query.filter_by(id=current_user.get_id())
        user.update(user_profile_schema_instance.data)
        try:
            db.session.commit()
            return jsonify({"message":"Profile successfully updated"}) 
        except:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO UPDATE USER"))