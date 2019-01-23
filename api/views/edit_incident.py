import os

from flask import Blueprint, jsonify, json, request
from werkzeug import secure_filename

from api.helpers.auth_token import (
    non_admin,
    get_current_identity,
    token_required,
)
from api.helpers.validation import (
    request_data_required,
    is_valid_uuid,
    validate_edit_location
)
from api.models.incident import Incident

incident_obj = Incident()
edit_bp = Blueprint(
    "edit_bp", __name__, url_prefix="/api/v2"
)


@edit_bp.route(
    "/red-flags/<red_flag_id>/location", methods=["PATCH"]
)
@token_required
@non_admin
@is_valid_uuid
@request_data_required
def edit_red_flag_location(red_flag_id):
    data = request.get_json(force=True)
    is_invalid_location = validate_edit_location(data.get("location"))

    results = incident_obj.get_incident_by_id(inc_id=red_flag_id, inc_type='red-flag')
    response = None

    if not results:
        response = (
            jsonify(
                {
                    "status": 404,
                    "error": "red-flag record does not exist",
                }
            ),
            404,
        )
    elif is_invalid_location:
        response = (
            jsonify({"error": is_invalid_location, "status": 400}),
            400,
        )

    elif (
            results["created_by"] == get_current_identity()
            and results["status"].lower() == "draft"
    ):
        location = data.get("location")

        inc_id = red_flag_id
        updated_record = incident_obj.update_incident_location(
            inc_id=inc_id, inc_type='red-flag', location=location
        )


        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": updated_record['id'],
                            "location":updated_record['location'],
                            "message": "Updated red-flag record’s location"
                        }
                    ],
                }
            ),
            200,
        )
    else:
        response = (
            jsonify(
                {
                    "status": 403,
                    "error": "You are not allowed to modify this resource",
                }
            ),
            403,
        )
    return response
