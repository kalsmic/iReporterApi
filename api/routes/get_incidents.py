from flask import Blueprint, jsonify

from api.helpers.auth_token import token_required
from api.models.incident import (
    red_flags,
    get_incident_record,
    get_all_incident_records,
)

get_red_flags_bp = Blueprint(
    "get_red_flags_bp", __name__, url_prefix="/api/v1"
)


@get_red_flags_bp.route("/red-flags", methods=["GET"])
@token_required
def get_all_red_flags():
    return (
        jsonify({"status": 200, "data": get_all_incident_records(red_flags)}),
        200,
    )


@get_red_flags_bp.route("/red-flags/<red_flag_id>", methods=["GET"])
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
    response = None
    if results:
        response = jsonify({"status": 200, "data": [results]}), 200
    else:

        response = (
            jsonify(
                {"status": 404, "error": "Red-flag record does not exist"}
            ),
            404,
        )

    return response
