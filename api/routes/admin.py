from flask import Blueprint, jsonify, json, request

from api.helpers.auth_token import admin_required, token_required
from api.helpers.validation import (
    request_data_required,
    is_valid_status,
    is_valid_id,
)
from api.models.incident import get_incident_obj_by_id, red_flags
from api.helpers.responses import wrong_status

admin_flags_bp = Blueprint("admin_flags_bp", __name__, url_prefix="/api/v1")


@admin_flags_bp.route("/red-flags/<red_flag_id>/status", methods=["PATCH"])
@token_required
@admin_required
@request_data_required
def edit_red_flag_status(red_flag_id):
    record_id = red_flag_id
    if not is_valid_id(record_id):
        return (
            jsonify({"error": "Red-flag id must be an number", "status": 400}),
            400,
        )

    status = json.loads(request.data).get("status")

    incident_id = int(red_flag_id)
    incident_results = get_incident_obj_by_id(int(incident_id), red_flags)

    response = None
    if not incident_results or not incident_results.incident_id == incident_id:
        response = (
            jsonify(
                {"status": 404, "error": "Red-flag record does not exist"}
            ),
            404,
        )
    elif not is_valid_status(status):
        response = jsonify({"status": 400, "error": wrong_status}), 400

    else:

        incident_results.status = status
        incident_results.status = status.lower()

        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": incident_results.incident_id,
                            "message": "Updated red-flag record’s status",
                        }
                    ],
                }
            ),
            200,
        )

    return response
