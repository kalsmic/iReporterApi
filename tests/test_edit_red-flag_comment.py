from flask import json

from .base import user1_header, user2_header

from api.helpers.responses import invalid_token_message


# EDIT A RED-FLAG RECORD'S COMMENT
def test_edit_a_red_flag_comment_without_a_token(client):
    response = client.patch("api/v1/red-flags/2/comment")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_edit_a_red_flag_comment_with_an_invalid_red_flag_id(client):
    response = client.patch(
        "api/v1/red-flags/f/comment",
        headers=user1_header,
        data=json.dumps({"comment": "I disagree"}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Red-flag id must be an number"


#
def test_edit_a_red_flag_comment_without_comment_data(client):
    response = client.patch("api/v1/red-flags/2/comment", headers=user1_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide valid input data"


def test_edit_a_red_flag_comment_for_a_red_flag_record_which_does_not_exist(
    client
):
    response = client.patch(
        "api/v1/red-flags/10/comment",
        headers=user1_header,
        data=json.dumps({"comment": "I disagree"}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "Red-flag record does not exist"


def test_edit_a_red_flag_comment_for_a_red_flag_record_with_without_a_comment(
    client
):
    response = client.patch(
        "api/v1/red-flags/2/comment",
        headers=user1_header,
        data=json.dumps({"comment": ""}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide a comment"


def test_edit_a_red_flag_comment_created_by_another_user(client):
    response = client.patch(
        "api/v1/red-flags/2/comment",
        headers=user2_header,
        data=json.dumps({"comment": "I diasgree"}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You can only edit comments created by you"


def test_edit_a_red_flag_comment_created_by_the_current_user(client):
    response = client.patch(
        "api/v1/red-flags/2/comment",
        headers=user1_header,
        data=json.dumps({"comment": "I diasgree"}),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["message"] == "Updated red-flag record’s comment"


def test_edit_a_red_flag_comment_with_status_other_than_draft(client):
    response = client.patch(
        "api/v1/red-flags/1/comment",
        headers=user2_header,
        data=json.dumps({"comment": "I diasgree"}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    err = "You cannot edit a record which is under investigation"
    assert data["error"] == err
