from flask import Blueprint, jsonify, json, request

from api.helpers.auth_token import (
    token_required,
    non_admin,
    get_current_identity,
)

red_flags_bp = Blueprint("red_flags_bp", __name__, url_prefix="/api/v1")
from api.models.incident import (
    RedFlag,
    incident_record_exists,
    red_flags,
    get_incident_record,
    get_all_incident_records,
    get_incident_obj_by_id,
)
from api.helpers.validation import (
    validate_new_incident,
    is_valid_id,
    validate_edit_location,
    request_data_required,
    validate_comment,
)

from api.helpers.responses import (
    expected_new_incident_format,
    delete_not_allowed,
)


@red_flags_bp.route("/red-flags", methods=["POST"])
@token_required
@non_admin
def new_red_flag():
    if not request.data:
        return (
            jsonify(
                {
                    "error": "Please provide RedFlag Data",
                    "expected": expected_new_incident_format,
                    "status": 400,
                }
            ),
            400,
        )
    data = json.loads(request.data)

    new_red_flag_data = {
        "title": data.get("title"),
        "description": data.get("description"),
        "location": data.get("location"),
        "comment": data.get("comment"),
        "tags": data.get("tags"),
        "images": data.get("Images"),
        "videos": data.get("Videos"),
    }

    not_valid = validate_new_incident(**new_red_flag_data)

    if not_valid:
        return not_valid
    response = None
    if not incident_record_exists(
        new_red_flag_data["title"], new_red_flag_data["description"], red_flags
    ):
        new_red_flag_data["user_id"] = get_current_identity()
        new_record = RedFlag(**new_red_flag_data)
        red_flags.append(new_record)

        response = (
            jsonify(
                {
                    "status": 201,
                    "data": [
                        {
                            "id": new_record.incident_id,
                            "message": "Created red-flag record",
                        }
                    ],
                }
            ),
            201,
        )
    else:

        response = (
            jsonify(
                {"status": 409, "error": "Red-flag record already exists"}
            ),
            409,
        )

    return response


@red_flags_bp.route("/red-flags", methods=["GET"])
@token_required
def get_all_red_flags():
    return (
        jsonify({"status": 200, "data": get_all_incident_records(red_flags)}),
        200,
    )


@red_flags_bp.route("/red-flags/<red_flag_id>", methods=["GET"])
@token_required
def get_a_red_flag(red_flag_id):
    try:
        red_flag_id = int(red_flag_id)
    except ValueError:
        return (
            jsonify(
                {"status": 400, "error": "Red-flag id must be an integer"}
            ),
            400,
        )

    results = get_incident_record(red_flag_id, red_flags)
    if results:
        return jsonify({"status": 200, "data": [results]}), 200
    return (
        jsonify({"status": 404, "error": "Red-flag record does not exist"}),
        404,
    )
