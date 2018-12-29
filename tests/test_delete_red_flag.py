from flask import json

from api.helpers.responses import invalid_token_message
from .base import user2_header, user1_header


# DELETE A RED FLAG RECORD


def test_delete_red_flag_without_a_access_token(client):
    #
    response = client.delete("api/v1/red-flags/1")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_delete_red_flag_with_red_flag_id_which_does_not_exist(client):
    # red flag id does not exist
    response = client.delete("api/v1/red-flags/46", headers=user1_header)
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "Red-flag record does not exist"


def test_delete_red_flag_with_invalid_format_red_flag_id(client):
    response = client.delete("api/v1/red-flags/fdf", headers=user1_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Red-flag id must be an integer"


def test_delete_red_flag_for_another_user(client):
    response = client.delete("api/v1/red-flags/2", headers=user2_header)
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You are not allowed to delete this resource"


def test_delete_red_flag_for_with_status_other_than_draft(client):
    response = client.delete("api/v1/red-flags/1", headers=user2_header)
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == (
        "You are not allowed to delete a red-flag which is under "
        "investigation"
    )


def test_delete_red_flag(client):
    response = client.delete("api/v1/red-flags/4", headers=user1_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["message"] == "red-flag record has been deleted"
