from flask import json

from api.helpers.responses import invalid_token_message
from .base import user2_header, user1_header


# EDIT A RED-FLAG RECORD'S LOCATION
def test_edit_a_red_flag_location_without_a_token(client):
    response = client.patch("api/v1/red-flags/2/location")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == invalid_token_message


def test_edit_a_red_flag_location_without_location_data(client):
    response = client.patch(
        "api/v1/red-flags/2/location", headers=user1_header
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide a valid location"


def test_edit_a_red_flag_location_which_does_not_exist(client):
    response = client.patch(
        "api/v1/red-flags/12/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "Red-flag record does not exist"


def test_edit_a_red_flag_location_which_does_not_belong_to_user(client):
    response = client.patch(
        "api/v1/red-flags/2/location",
        headers=user2_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You are not allowed to modify this resource"


def test_edit_a_red_flag_location_with_invalid_red_flag_id(client):
    response = client.patch(
        "api/v1/red-flags/df/location",
        headers=user2_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Red-flag id must be an integer"


def test_edit_a_red_flag_location_status_of_draft(client):
    response = client.patch(
        "api/v1/red-flags/2/location",
        headers=user1_header,
        data=json.dumps({"location": [12, 23]}),
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["message"] == "Updated red-flag record’s location"
    assert data["data"][0]["red-flag"]["id"] == 2
    assert data["data"][0]["red-flag"]["location"] == [12, 23]


def test_edit_a_red_flag_location_with_invalid_location_coordinates(client):
    response = client.patch(
        "api/v1/red-flags/2/location",
        headers=user1_header,
        data=json.dumps({"location": [-90, 12]}),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == (
        "latitude must be between -90 and 90 and longitude"
        " coordinates must be between -180 and 180"
    )


def test_edit_a_red_flag_location_status_other_than_draft(client):
    response = client.patch(
        "api/v1/red-flags/1/location",
        headers=user2_header,
        data=json.dumps({"location": [12, 12]}),
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You are not allowed to modify this resource"
