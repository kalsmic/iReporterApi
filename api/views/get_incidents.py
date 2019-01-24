from flask import Blueprint, jsonify

from api.helpers.auth_token import token_required
from api.models.incident import Incident
from api.helpers.validation import is_valid_uuid,parse_incident_type

get_inc_bp = Blueprint(
    "get_incidents", __name__, url_prefix="/api/v2"
)

incident_obj = Incident()


@get_inc_bp.route("/<incident_type>", methods=["GET"])
@token_required
@parse_incident_type
def get_all_red_flags(incident_type):
    incident_type = incident_type[:-1]

    results = incident_obj.get_all_incident_records(
        inc_type=incident_type
    )

    return jsonify({"status": 200, "data": results}), 200


@get_inc_bp.route("/red-flags/<red_flag_id>", methods=["GET"])
@token_required
@is_valid_uuid
def get_a_red_flag(red_flag_id):
    results = incident_obj.get_an_incident_record_(
        inc_type='red-flag', inc_id=red_flag_id
    )
    response = None
    if results and 'error' in results:
        response = (
            jsonify(
                {
                    "status": 401,
                    "error": results['error'],
                }
            ),
            401,
        )
    elif results:
        response = jsonify({"status": 200, "data": [results]}), 200
    else:

        response = (
            jsonify(
                {
                    "status": 404,
                    "error": "red-flag record does not exist",
                }
            ),
            404,
        )

    return response

