from flask import Blueprint, jsonify

from api.helpers.auth_token import (
    token_required,
    non_admin,
    get_current_identity,
)
from api.helpers.responses import delete_not_allowed
from api.helpers.validation import is_valid_id
from api.models.incident import red_flags, get_incident_obj_by_id

delete_red_flag_bp = Blueprint(
    "delete_red_flag_bp", __name__, url_prefix="/api/v1"
)


@delete_red_flag_bp.route("/red-flags/<red_flag_id>", methods=["DELETE"])
@token_required
@non_admin
@is_valid_id
def delete_record(red_flag_id):
    results = get_incident_obj_by_id(
        incident_id=int(red_flag_id), collection=red_flags
    )

    response = None
    if not results:
        response = (
            jsonify(
                {"status": 404, "error": "Red-flag record does not exist"}
            ),
            404,
        )
    elif not results.created_by == get_current_identity():

        response = (jsonify({"status": 403, "error": delete_not_allowed}), 403)
    elif results.status == "draft":
        record_id = results.incident_id
        record_index = red_flags.index(results)
        red_flags.pop(record_index)

        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": record_id,
                            "message": "red-flag record has been deleted",
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
                    "error": (
                        "You are not allowed to delete a red-flag which is"
                        f" {results.status }"
                    ),
                }
            ),
            403,
        )
    return response
