from flask import json

from api.helpers.responses import invalid_token_message, expired_token_message
from .base import (
    user2_header,
    expired_token_header,
    user1_header,
    user1_id,
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
