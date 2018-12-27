from flask import Blueprint, jsonify, json, request

from api.helpers.auth_token import (
    token_required,
    non_admin,
    get_current_identity,
)

edit_red_flags_bp = Blueprint(
    "edit_red_flags_bp", __name__, url_prefix="/api/v1"
)
from api.models.incident import red_flags, get_incident_obj_by_id
from api.helpers.validation import (
    is_valid_id,
    validate_edit_location,
    request_data_required,
    validate_comment,
)


@edit_red_flags_bp.route(
    "/red-flags/<red_flag_id>/location", methods=["PATCH"]
)
@token_required
@non_admin
def edit_red_flag_location(red_flag_id):
    record_id = red_flag_id

    if not is_valid_id(record_id):
        return (
            jsonify({"error": "Red-flag id must be an number", "status": 400}),
            400,
        )

    data = request.data
    is_invalid = validate_edit_location(data)
    results = get_incident_obj_by_id(int(record_id), red_flags)

    response = None

    if not results:
        response = (
            jsonify(
                {"status": 404, "error": "Red-flag record does not exist"}
            ),
            404,
        )
    elif is_invalid:
        response = (jsonify({"error": is_invalid, "status": 400}), 400)

    elif (
        results.created_by == get_current_identity()
        and results.status == "draft"
    ):
        location = json.loads(data).get("location")

        results.location = location
        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": results.incident_id,
                            "message": "Updated red-flag record’s location",
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


@edit_red_flags_bp.route("/red-flags/<red_flag_id>/comment", methods=["PATCH"])
@token_required
@non_admin
@request_data_required
def edit_red_flag_comment(red_flag_id):
    record_id = red_flag_id
    if not is_valid_id(record_id):
        return (
            jsonify({"error": "Red-flag id must be an number", "status": 400}),
            400,
        )

    data = request.data
    comment = json.loads(data).get("comment")
    is_invalid = validate_comment(comment, edit=1)
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
    elif is_invalid:
        response = (jsonify({"error": is_invalid, "status": 400}), 400)

    elif not incident_results.created_by == get_current_identity():
        response = (
            jsonify(
                {
                    "status": 403,
                    "error": "You can only edit comments created by you",
                }
            ),
            403,
        )
    elif not incident_results.status == "draft":
        response = (
            jsonify(
                {
                    "status": 403,
                    "error": (
                        "You cannot edit a record which is"
                        f" {incident_results.status }"
                    ),
                }
            ),
            403,
        )
    else:
        comment = json.loads(data).get("comment")
        incident_results.comment = comment

        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": incident_results.incident_id,
                            "message": "Updated red-flag record’s comment",
                        }
                    ],
                }
            ),
            200,
        )

    return response
