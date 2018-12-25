from flask import Blueprint, jsonify, json, request

from api.helpers.auth_token import token_required, non_admin, get_current_identity

red_flags_bp = Blueprint("red_flags_bp", __name__, url_prefix="/api/v1")
from api.models.incident import (
    RedFlag,
    Comment,
    incident_record_exists,
    red_flags,
    comments,
    get_incident_record,
    get_all_incident_records,
)
from api.helpers.validation import validate_new_incident

from api.helpers.responses import expected_new_incident_format


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

    title = data.get("title")
    tags = data.get("tags")
    description = data.get("description")
    images = data.get("Images", "")
    videos = data.get("Videos", "")
    location = data.get("location", "")
    comment = data.get("comment", "")

    not_valid = validate_new_incident(
        title=title,
        description=description,
        location=location,
        comment=comment,
        tags=tags,
        images=images,
        videos=videos,
    )

    if not_valid:
        return not_valid

    if not incident_record_exists(title, description, red_flags):
        new_record = RedFlag(
            title=title,
            description=description,
            location=location,
            tags=tags,
            videos=videos,
            images=images,
            user_id=get_current_identity(),
        )
        red_flags.append(new_record)
        if comment:
            new_comment = Comment(new_record.incident_id, 1, comment)
            comments.append(new_comment)

        return (
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

    return jsonify({"status": 409, "error": "Red-flag record already exists"}), 409


@red_flags_bp.route("/red-flags", methods=["GET"])
@token_required
def get_all_red_flags():
    return jsonify({"status": 200, "data": get_all_incident_records(red_flags)}), 200


@red_flags_bp.route("/red-flags/<red_flag_id>", methods=["GET"])
@token_required
def get_a_red_flag(red_flag_id):
    try:
        red_flag_id = int(red_flag_id)
    except ValueError:
        return (
            jsonify({"status": 400, "error": "Red-flag id must be an integer"}),
            400,
        )

    results = get_incident_record(red_flag_id, red_flags)
    if results:
        return jsonify({"status": 200, "data": [results]}), 200
    return (jsonify({"status": 404, "error": "Red-flag record does not exist"}), 404)
