from flask import (
    Blueprint,
    jsonify,
    json,
    request
)

from api.helpers import (
    token_required,
    request_data_required,
    non_admin
)

red_flags_bp = Blueprint('red_flags_bp', __name__, url_prefix='/api/v1')
from api.models.incident import (
    RedFlag,
    check_if_new_red_flag_exists,
    get_all_record,
    get_a_specific_red_flag
)


@red_flags_bp.route('/red-flags', methods=['POST'])
@token_required
@non_admin
@request_data_required
def new_red_flag():

    data = json.loads(request.data)

    red_flags_data = RedFlag(location=data.get('location'), comment=data.get('comment'))
    is_not_valid_location = red_flags_data.validate_location()
    if is_not_valid_location:
        return jsonify({"status": 400, "message": is_not_valid_location}), 400
    is_not_valid_comment = red_flags_data.validate_comment()

    if is_not_valid_comment:
        return jsonify({"status": 400, "message": is_not_valid_comment}), 400

    if check_if_new_red_flag_exists(red_flags_data):
        return jsonify({"status": 400, "error": "Red-flag record already exists"}), 400
    red_flags_data.add_red_flag()

    return jsonify({
        "status": 201,
        "data": [{
            "id": red_flags_data.id,
            "message": "Created red-flag record"}], }), 201


@red_flags_bp.route('/red-flags', methods=['GET'])
@token_required
def get_all_red_flags():
    return jsonify({
        "status": 200,
        "data": get_all_record()}), 200


@red_flags_bp.route('/red-flags/<int:red_flag_id>', methods=['GET'])
# @token_required
def get_a_red_flag(red_flag_id):
    results = get_a_specific_red_flag(red_flag_id)
    if results:
        return jsonify({
            "status": 200,
            "data": [results]
        }), 200
    return jsonify({
        "status": 404,
        "error": "Red-flag record does not exist"
    }), 404
