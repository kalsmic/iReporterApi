from flask import json

from api.helpers.responses import invalid_token_message, expired_token_message
from .base import (
    user2_header,
    expired_token_header,
    user1_header,
    user1_id,
    admin_header,
)


# GET ALL RED-FLAG RECORDS


def test_get_all_red_flags_without_token(client):
    # test only logged in user get red flags
    response = client.get("api/v2/red-flags")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": invalid_token_message, "status": 401}


def test_get_all_red_flags_with_expired_token(client):
    # test only logged in user get red flags
    response = client.get("api/v2/red-flags", headers=expired_token_header)
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": expired_token_message, "status": 401}


def test_get_all_red_flags(client):
    response = client.get("api/v2/red-flags", headers=user1_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"][0]["created_by"] == user1_id

    response = client.get("api/v2/red-flags", headers=user2_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"] == []


# GET A SPECIFIC RED-FLAG RECORD


def test_get_a_red_flag(client):
    response = client.get(
        "api/v2/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb",
        headers=user1_header,
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert (
            data["data"][0]["title"]
            == "Vestibulum blandit ligula a mollis ullamcorper."
    )


def test_get_a_red_flag_for_another_user(client):
    response = client.get(
        "api/v2/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb",
        headers=user2_header,
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == "You're not Authorized to access this resource"


def test_admin_get_a_red_flag(client):
    response = client.get(
        "api/v2/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb",
        headers=admin_header,
    )
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert (
            data["data"][0]["title"]
            == "Vestibulum blandit ligula a mollis ullamcorper."
    )


# INTERVENTIONS

def test_get_all_interventions_without_token(client):
    # test only logged in user get red flags
    response = client.get("api/v2/interventions")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": invalid_token_message, "status": 401}


def test_get_all_interventions_with_expired_token(client):
    # test only logged in user get red flags
    response = client.get("api/v2/interventions", headers=expired_token_header)
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": expired_token_message, "status": 401}


def test_get_all_interventions(client):
    response = client.get("api/v2/interventions", headers=user1_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"][0]["created_by"] == user1_id

    response = client.get("api/v2/interventions", headers=user2_header)
    assert response.status_code == 200
    assert isinstance(data["data"],list)

