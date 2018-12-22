from flask import json

from api.models.incident import red_flags
from .base import (
    admin_header,
    user2_header,
    user1_header,
    user1_id,
    user2_id,
)

comment = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""

comment1 = """Volutpat sed cras ornare arcu. Varius vel pharetra vel turpis nunc. Facilisi nullam vehicula ipsum a arcu."""
comment2 = """Libero nunc consequat interdum varius sit amet mattis vulputate enim"""
comment3 = """honcus aenean vel elit scelerisque. Pellentesque sit amet porttitor eget"""
valid_data = {"location": "12.767 12.667", "comment": comment}

empty_location = {"location": " ", "comment": comment}
valid_data = {"location": "12.767 12.667", "comment": comment}
valid_data1 = {"location": "12.767 12.667", "comment": comment1}
valid_data2 = {"location": "12.777 12.667", "comment": comment2}
valid_data3 = {"location": "12.767 12.667", "comment": comment3}

invalid_location = {"location": "12212", "comment": comment}
with_no_comment = {"location": "12.3 34.5"}





def test_create_a_red_flag(client):
    # test only logged in user with token
    response = client.post("api/v1/red-flags",)
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": "Invalid Token verification failed", "status": 401}



    # test admin cannot create a red flag
    response = client.post("api/v1/red-flags",headers = admin_header,data=json.dumps(valid_data))
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data == {'error': 'Admin cannot access this resource', 'status': 403}


    # create a red flag with no data
    response = client.post("api/v1/red-flags", headers=user1_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Provide provide valid data"

    # create a red flag with one coordinate in the location
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(invalid_location))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["message"] == "location must contain both latitude and longitude"

    # create a red flag with coordinate containing a letter
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(invalid_location))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["message"] == "location must contain both latitude and longitude"

    # create a red flag with no_comment
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(with_no_comment))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["message"] == "Please provide a comment"

    # create a red flag with valid data
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(valid_data))
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert "id" in data["data"][0]
    assert data["data"][0]["message"] == "Created red-flag record"
    red_flags[0].createdBy = 1

    # create duplicate red flags
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(valid_data))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Red-flag record already exists"


def test_get_all_red_flags(client):
    # test only logged in user get red flags
    response = client.get("api/v1/red-flags")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": "Invalid Token verification failed", "status": 401}

    # create red flag records for various users
    record1 = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(valid_data1))
    record2 = client.post("api/v1/red-flags", headers=user2_header, data=json.dumps(valid_data2))
    record3 = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(valid_data3))

    # confirm record for testing have been created
    assert record1.status_code == 201
    assert record2.status_code == 201
    assert record3.status_code == 201

    # get all redflags user1
    response = client.get("api/v1/red-flags", headers=user2_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"][0]["createdBy"] == user2_id

    # get all redflags user1
    response = client.get("api/v1/red-flags", headers=user1_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"][0]["createdBy"] == user1_id
#
#
#
def test_get_a_red_flag(client):
    # record exists and user can get only their record
    response = client.get("api/v1/red-flags/12",headers=user2_header)
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["error"] == "Red-flag record does not exist"
    #
    # record exists and user can get only their record
    response = client.get("/api/v1/red-flags/1", headers=user1_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"][0]["createdBy"] == 1
    assert data["data"][0]["comment"] == "my first red flag incident"