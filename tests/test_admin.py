from flask import json

from api.helpers.responses import wrong_status, invalid_token_message

from .base import user1_header, admin_header


# EDIT A RED-FLAG RECORD'S STATUS
def test_edit_a_red_flag_status_without_a_token(client):
    response = client.patch("api/v1/red-flags/2/status")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_non_admin_edit_a_red_flag_status(client):
    response = client.patch(
        "api/v1/red-flags/1/status",
        headers=user1_header,
        data=json.dumps({"status": "resolved"}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "Only Admin can access this resource"


def test_edit_a_red_flag_status_with_an_invalid_red_flag_id(client):
    response = client.patch(
        "api/v1/red-flags/f/status",
        headers=admin_header,
        data=json.dumps({"status": "resolved"}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Red-flag id must be an number"


#
def test_edit_a_red_flag_status_without_request_data(client):
    response = client.patch("api/v1/red-flags/2/status", headers=admin_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide valid input data"


def test_edit_a_red_flag_status_with_invalid_status_data(client):
    response = client.patch(
        "api/v1/red-flags/2/status",
        headers=admin_header,
        data=json.dumps({"status": "I disagree"}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == wrong_status

    response = client.patch(
        "api/v1/red-flags/3/status",
        headers=admin_header,
        data=json.dumps({"status": 1}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == wrong_status


def test_edit_a_red_flag_status_for_a_red_flag_record_which_does_not_exist(
    client
):
    response = client.patch(
        "api/v1/red-flags/10/status",
        headers=admin_header,
        data=json.dumps({"status": "resolved"}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "Red-flag record does not exist"


def test_edit_a_red_flag_status(client):
    response = client.patch(
        "api/v1/red-flags/3/status",
        headers=admin_header,
        data=json.dumps({"status": "resolved"}),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["message"] == "Updated red-flag record’s status"
