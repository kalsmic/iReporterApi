# "File contails validation functions"
# def contains_digit(s):
#     isdigit = str.isdigit
#     return any(map(isdigit,s))
#
# def verify_phone_number(phone_number):
import re
from flask import (
    request,
    jsonify,
    json
)
from api.models.user import (
    check_if_email_exists,
    check_if_username_exists,
    register_user
)


def is_valid_login_data():
    """Verify login data"""
    if not request.data:
        return jsonify({
            'error': "Please provide valid data",
            "status": 400
        }), 400

    new_user = json.loads(request.data)

    try:
        firstname = new_user['firstname']
        lastname = new_user['lastname']
        othername = new_user['othername']
        username = new_user['username']
        email = new_user['email']
        phoneNumber = new_user['phoneNumber']
        password = new_user['password']

    except KeyError:
        return jsonify({
            'error': "Please provide the correct keys for the data",
            "status": 400
        }), 400

    if not firstname or not lastname or not firstname.isalpha() or not lastname.isaplha():
        # checks if name fields  do not contains any space,or is empty
        return jsonify({
            'error': "Name fields cannot be empty or contain any space character",
            "status": 400
        }), 400

    elif othername and not othername.isalpha():
        # other name is optional but must be contain only letters if provided
        return jsonify({
            'error': "Name must contain letter characters only",
            "status": 400
        }), 400

    elif not username or username.isspace():
        # email must not contain any space or be empty
        return jsonify({
            'error': "username cannot be empty or contain any a space in it",
            "status": 400
        }), 400

    elif check_if_username_exists(username):
        # username must be unique
        return jsonify({
            'error': " username already taken",
            "status": 400
        }), 400

    elif not email or not re.match('[^@]+@[^@]+\.[^@]+', email):
        # email must be of valid pattern
        return jsonify({
            'error': " please provide a valid email",
            "status": 400
        }), 400
    elif check_if_email_exists(email):
        # email must be unique
        return jsonify({
            'error': " Email already exists",
            "status": 400
        }), 400

    elif not phoneNumber:
        return jsonify({
            'error': " phoneNumber cannot be empty",
            "status": 400
        }), 400
    elif not phoneNumber[0] != '0':
        return jsonify({
            'error': " phoneNumber must start with a zero",
            "status": 400
        }), 400
    elif not len(phoneNumber) == 10 or not phoneNumber[1:].isdigit():
        return jsonify({
            'error': " phoneNumber must be a string of ten numbers only",
            "status": 400
        }), 400

    elif not password or password.isspace():
        return jsonify({
            'error': " password cannot be empty or contain a space in it",
            "status": 400
        }), 400
    elif len(password) < 8:
        return jsonify({
            'error': " password must be at least 8 characters long",
            "status": 400
        }), 400
    else:
        user = User()
