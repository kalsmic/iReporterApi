"""Module contains functions for validating user input"""
import re
from functools import wraps

from flask import jsonify, request, json

from api.helpers.responses import (
    expected_new_incident_format,
    wrong_password,
    wrong_username,
    wrong_email,
    wrong_phone_number,
    wrong_name,
    wrong_description,
)


def request_data_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.data:
            return (
                jsonify(
                    {"error": "Please provide valid input data", "status": 400}
                ),
                400,
            )
        return func(*args, **kwargs)

    return wrapper


def is_valid_id(record_id):
    try:
        int(record_id)
    except ValueError:
        return False
    return True


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
    if not email and not re.match("[^@]+@[^@]+\.[^@]+", email):
        return wrong_email
    return None


def validate_user_name(user_name):
    if user_name and not is_number(user_name) and len(user_name) >= 5:
        return None
    return wrong_username


def validate_name(name, required=1):
    error = wrong_name
    if not required and name == "":
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


def validate_comment(comment, edit=0):
    error = None
    if comment == "" and edit == 0:
        pass
    elif not comment and edit == 1:
        error = "Please provide a comment"
    elif not is_string(comment):
        error = "Comment must be a string"
    return error


def validate_sentence(sentence, required=0, min_len=0, max_len=0):
    error = None
    if str(sentence).isdigit():
        error = "Field cannot be a number"
    elif min_len == 0 and sentence == "" or sentence.isspace():
        pass
    elif required and not is_string(sentence):
        error = "Field cannot be blank"
    elif len(sentence) < min_len:
        error = f"Field must contain a minimum of {str(min_len)} characters"
    elif max_len and len(sentence) > max_len:
        error = f"Field must contain a maximum of {str(max_len)} characters"

    return error


def validate_description(description):
    error = None
    if not description or not is_string(description):
        error = wrong_description
    return error


media_format = {"Videos": [".mp4", "MP4"], "Images": ["jpg", "JPEG"]}


def is_validate_media_type(collection, media_type):
    for media in collection:
        if not media.endswith(media_format.get(media_type)[0]):
            return False
    return True


def validate_media(media_collection, media_type):
    media_format = {"Videos": [".mp4", "MP4"], "Images": ["jpg", "JPEG"]}
    error = None
    if not isinstance(media_collection, list):
        error = f"Please provide an empty list of {media_type} if none"
    elif not is_validate_media_type(media_collection, media_type):
        error = (
            f"Only {media_format.get(media_type)[1]} {media_type} are "
            "supported"
        )

    return error


def is_a_valid_tag(tags):
    for tag in tags:
        if not is_string(tag):
            return False
    return True


def validate_tags(tags):
    error = None
    if not isinstance(tags, list):
        error = (
            "Please provide a list of tags i.e ['crime','rape'] or an "
            "empty list"
        )
    elif not is_a_valid_tag(tags):
        error = "Tags must be of string type i.e ['crime','rape']"
    return error


def validate_location(location):
    error = None
    if not isinstance(location, list) or not len(location) == 2:
        error = (
            "location must be a list with both Latitude and Longitude "
            "coordinates"
        )
    elif not is_number(location[0]) or not is_number(location[1]):
        error = "location coordinates must be a number"
    elif not -90 < location[0] < 90 or not -180 < location[1] < 180:
        error = (
            "latitude must be between -90 and 90 and longitude "
            "coordinates must be between -180 and 180"
        )

    return error


def validate_new_user(*args, **kwargs):
    errors = {}
    errors["firstname"] = validate_name(kwargs["first_name"])
    errors["lastname"] = validate_name(kwargs["last_name"])
    errors["othernames"] = validate_name(kwargs["other_names"], 0)
    errors["username"] = validate_user_name(kwargs["user_name"])
    errors["password"] = validate_password(kwargs["password"])
    errors["email"] = validate_email(kwargs["email"])
    errors["phoneNumber"] = validate_phone_number(kwargs["phone_number"])
    invalid_fields = {key: value for key, value in errors.items() if value}
    if invalid_fields:
        return (jsonify({"status": 400, "error": invalid_fields}), 400)
    return None


def validate_new_incident(**kwargs):
    errors = {}
    errors["title"] = validate_sentence(kwargs.get("title"), 1, 4, 100)
    errors["description"] = validate_description(kwargs.get("description"))
    errors["location"] = validate_location(kwargs.get("location"))
    errors["tags"] = validate_tags(kwargs.get("tags"))
    errors["Images"] = validate_media(kwargs.get("images"), "Images")
    errors["Videos"] = validate_media(kwargs.get("videos"), "Videos")
    errors["comment"] = validate_comment(kwargs.get("comment"))
    not_valid = {key: value for key, value in errors.items() if value}

    if not_valid:
        return (
            jsonify(
                {
                    "status": 400,
                    "error": not_valid,
                    "expected": expected_new_incident_format,
                }
            ),
            400,
        )
    return None


def validate_edit_location(data):
    error = None
    if not data:
        error = "Please provide a valid location"
    else:
        error = validate_location(json.loads(data).get("location"))
    return error


def is_valid_status(status):
    is_valid = True
    if not status or not isinstance(status, str):
        is_valid = False
    elif str(status).lower() not in (
        "resolved",
        "under invenstigation",
        "rejected",
    ):
        is_valid = False
    return is_valid
