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
    get_incident_obj_by_id,
    get_comment_obj_by_id,
)
from api.helpers.validation import (
    validate_new_incident,
    is_valid_id,
    validate_edit_location,
    request_data_required,
    validate_comment,
)

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
            new_comment = Comment(
                new_record.incident_id, get_current_identity(), comment
            )
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


@red_flags_bp.route("/red-flags/<red_flag_id>/location", methods=["PATCH"])
@token_required
def edit_red_flag_location(red_flag_id):
    record_id = red_flag_id

    if not is_valid_id(record_id):
        return jsonify({"error": "Red-flag id must be an number", "status": 400}), 400

    data = request.data
    is_invalid = validate_edit_location(data)

    if is_invalid:
        return (jsonify({"error": is_invalid, "status": 400}), 400)

    results = get_incident_obj_by_id(int(record_id), red_flags)

    if not results:
        return (
            jsonify({"status": 404, "error": "Red-flag record does not exist"}),
            404,
        )

    if results.created_by == get_current_identity() and results.status == "draft":
        location = json.loads(data).get("location")

        results.location = location
        return (
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
    return (
        jsonify(
            {"status": 403, "error": "You are not allowed to modify this resource"}
        ),
        403,
    )


@red_flags_bp.route("/red-flags/<red_flag_id>/comment/<comment_id>", methods=["PATCH"])
@token_required
@request_data_required
def edit_red_flag_comment(red_flag_id, comment_id):
    record_id = red_flag_id
    if not is_valid_id(record_id):
        return jsonify({"error": "Red-flag id must be an number", "status": 400}), 400

    data = request.data

    # if 'comment' not in data
    comment = json.loads(data).get("comment")

    is_invalid = validate_comment(comment, edit=1)

    if is_invalid:
        return (jsonify({"error": is_invalid, "status": 400}), 400)

    comment_id, incident_id = int(comment_id), int(red_flag_id)
    comment_results = get_comment_obj_by_id(
        comment_id=comment_id, incident_id=incident_id
    )
    incident_results = get_incident_obj_by_id(int(record_id), red_flags)

    response = None
    if not incident_results or not incident_results.incident_id == incident_id:
        response = (
            jsonify({"status": 404, "error": "Red-flag record does not exist"}),
            404,
        )

    elif not incident_results.status == "draft":
        response = (
            jsonify(
                {
                    "status": 403,
                    "error": f"You cannot edit a record which is {incident_results.status }",
                }
            ),
            403,
        )
    elif not comment_results:
        response = (jsonify({"status": 404, "error": "Comment does not exist"}), 404)
    elif comment_results.comment_by == get_current_identity():
        comment = json.loads(data).get("comment")
        comment_results.body = comment

        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "commentId": comment_results.comment_id,
                            "redFlagId": comment_results.incident_id,
                            "message": "Updated red-flag record’s comment",
                        }
                    ],
                }
            ),
            200,
        )

    else:
        response = (
            jsonify(
                {"status": 403, "error": "You can only edit comments created by you"}
            ),
            403,
        )

    return response
