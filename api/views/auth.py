from flask import Blueprint, jsonify, request, json

from api.helpers.auth_token import encode_token
from api.helpers.validation import validate_new_user, sign_up_data_required
from api.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/api/v2")
user_obj = User()


@users_bp.route("/auth/signup", methods=["POST"])
@sign_up_data_required
def register_user():
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
    user_exists = user_obj.check_if_user_exists(
        new_user["user_name"], new_user["email"], new_user["phone_number"]
    )
    response = None
    if user_exists:
        response = jsonify({"error": user_exists, "status": 409}), 409
    else:

        new_user_details = user_obj.insert_user(**new_user)
        response = (
            jsonify(
                {
                    "status": 201,
                    "data": [
                        {
                            "user": new_user_details,
                            "token": encode_token(new_user_details["id"]),
                            "message": "Account created Successfully",
                        }
                    ],
                }
            ),
            201,
        )
    return response
