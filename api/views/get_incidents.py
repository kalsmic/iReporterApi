from flask import Blueprint, jsonify

from api.helpers.auth_token import token_required
from api.models.incident import Incident

get_inc_bp = Blueprint(
    "get_incidents", __name__, url_prefix="/api/v2"
)

incident_obj = Incident()


@get_inc_bp.route("/red-flags", methods=["GET"])
@token_required
def get_all_red_flags():
    results = incident_obj.get_all_incident_records(
        inc_type='red-flag'
    )

    return jsonify({"status": 200, "data": results}), 200



