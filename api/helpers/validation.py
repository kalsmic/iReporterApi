"""Module contains functions for validating user input"""
import re
from functools import wraps

from flask import jsonify, request

from api.helpers.responses import (
    wrong_password,
    wrong_username,
    wrong_email,
    wrong_phone_number,
    wrong_name
)


def sign_up_data_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        if not request.data:

            response = (
                jsonify(
                    {
                        "error": "Provide provide valid data to register",
                        "status": 400,
                    }
                ),
                400,
            )
        else:
            response = func(*args, **kwargs)
        return response

    return wrapper


def is_number(num_value):
    """Checks if num_value is a number"""
    if isinstance(num_value, int) or isinstance(num_value, float):
        return True
    return False


def is_string(str_value):
    """Checks if input is a string"""
    if (
            str_value
            and isinstance(str_value, str)
            and not str(str_value).isspace()
            and not str_value.isnumeric()
    ):
        return True
    return False


def contains_space(str_value):
    """Checks if input contains a space"""
    if " " in str_value or len(str(str_value).split(" ")) > 1:
        return True
    return False


def contains_number(str_value):
    """Checks if input contains a space"""
    for character in str_value:
        if character.isdigit():
            return True
    return False


def validate_email(email):
    if not email or not re.match("[^@]+@[^@]+\.[^@]+", email):
        return wrong_email
    return None


def validate_user_name(user_name):
    if user_name and not is_number(user_name) and len(user_name) >= 5:
        return None
    return wrong_username


def validate_name(name, required=1):
    error = wrong_name
    if not required and len(str(name).strip()) == 0:
        error = None
    elif (
            name
            and is_string(name)
            and not contains_space(name)
            and not contains_number(name)
    ):
        error = None
    return error


def validate_password(password):
    error = wrong_password
    if (
            len(password) >= 8
            and re.search("[A-Z]", password)
            and re.search("[0-9]", password)
            and re.search("[a-z]", password)
    ):
        error = None
    return error


def validate_phone_number(phone_number):
    error = wrong_phone_number

    if len(phone_number) == 10 and phone_number.isdigit():
        error = None
    return error


def validate_new_user(**kwargs):
    errors = dict()
    errors["firstname"] = validate_name(kwargs["first_name"])
    errors["lastname"] = validate_name(kwargs["last_name"])
    errors["othernames"] = validate_name(kwargs["other_names"], 0)
    errors["username"] = validate_user_name(kwargs["user_name"])
    errors["password"] = validate_password(kwargs["password"])
    errors["email"] = validate_email(kwargs["email"])
    errors["phoneNumber"] = validate_phone_number(kwargs["phone_number"])
    invalid_fields = {key: value for key, value in errors.items() if value}
    if invalid_fields:
        return jsonify({"status": 400, "error": invalid_fields}), 400
    return None
