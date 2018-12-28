from flask import Blueprint, jsonify, request, json

from api.helpers.auth_token import encode_token
from api.helpers.validation import validate_new_user
from api.models.user import (
    User,
    users,
    check_if_user_exists,
    is_valid_credentials,
)

users_bp = Blueprint("users_bp", __name__, url_prefix="/api/v1")


@users_bp.route("/auth/signup", methods=["POST"])
def register():
    expected_data = {
        "firstname": "String",
        "lastname": "String",
        "othernames": "String",
        "username": "String",
        "email": "String",
        "phoneNumber": "string",
        "password": "string",
    }
    if not request.data:
        return (
            jsonify(
                {
                    "error": "Provide provide valid data to register",
                    "expected": expected_data,
                    "status": 400,
                }
            ),
            400,
        )

    new_user = json.loads(request.data)
    try:
        first_name = new_user["firstname"]
        last_name = new_user["lastname"]
        other_names = new_user["othernames"]
        user_name = new_user["username"]
        email = new_user["email"]
        phone_number = new_user["phoneNumber"]
        password = new_user["password"]

    except KeyError:
        return (
            jsonify(
                {
                    "error": "Please provide the correct keys for the data",
                    "status": 422,
                }
            ),
            422,
        )

    new_user = {
        "first_name": first_name,
        "last_name": last_name,
        "other_names": other_names,
        "user_name": user_name,
        "email": email,
        "password": password,
        "phone_number": phone_number,
    }
    error = validate_new_user(**new_user)
    if error:
        return error
    user_exists = check_if_user_exists(
        user_name=new_user["user_name"], email=new_user["email"]
    )
    if user_exists:
        return jsonify({"error": user_exists, "status": 409}), 409

    new_user_obj = User(**new_user)
    users.append(new_user_obj)
    return (
        jsonify(
            {
                "status": 201,
                "data": [
                    {
                        "user": new_user_obj.get_user_details(),
                        "token": encode_token(new_user_obj.user_id,
                                              new_user_obj.is_admin),
                        "message": "Account created Successfully",
                    }
                ],
            }
        ),
        201,
    )


@users_bp.route("/auth/login", methods=["POST"])
def login():
    expected_data = {"username": "String", "password": "string"}
    if not request.data:
        return (
            jsonify(
                {
                    "error": "Provide provide valid data to login",
                    "expected": expected_data,
                    "status": 400,
                }
            ),
            400,
        )

    user_credentials = json.loads(request.data)
    response = None
    try:
        username = user_credentials["username"]
        password = user_credentials["password"]

        # submit credentials
        data = is_valid_credentials(username, password)
        if data:
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [{
                            "token": encode_token(data.user_id, data.is_admin),
                            "user": data.get_user_details(),
                            "message": "Logged in successfully",
                        }]

                    }
                ),
                200,
            )
        else:
            response = jsonify({"error": "Invalid credentials",
                                "status": 401}), 401

    except KeyError:
        response = (
            jsonify(
                {
                    "error": "Please provide the correct keys for the data",
                    "status": 422,
                }
            ),
            422,
        )
    return response
