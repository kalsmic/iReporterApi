from flask import Blueprint, jsonify, json, request

from api.helpers.auth_token import (
    token_required,
    non_admin,
    get_current_identity,
)

create_red_flags_bp = Blueprint(
    "create_red_flags_bp", __name__, url_prefix="/api/v1"
)
from api.models.incident import RedFlag, incident_record_exists, red_flags
from api.helpers.validation import validate_new_incident

from api.helpers.responses import expected_new_incident_format


@create_red_flags_bp.route("/red-flags", methods=["POST"])
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
    response = None

    if not_valid:
        response = not_valid
    elif not incident_record_exists(
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
