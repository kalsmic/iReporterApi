from flask import json

from api.helpers.responses import invalid_token_message
from .base import admin_header, user1_header, new_record,user1_id


# CREATE A RED-FLAG
def test_create_a_red_flag_without_a_token(client):
    # test only logged in user with token
    response = client.post("api/v1/red-flags")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": invalid_token_message, "status": 401}


def test_admin_cannot_create_a_red_flag(client):
    response = client.post(
        "api/v1/red-flags", headers=admin_header, data=json.dumps(new_record)
    )
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data == {
        "error": "Admin cannot access this resource",
        "status": 403,
    }


def test_create_a_red_flag_without_data(client):
    response = client.post("api/v1/red-flags", headers=user1_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Please provide RedFlag Data"


def test_create_a_red_flag_with_valid_data(client):
    new_record[
        "comment"
    ] = "Lorem ipsum eiusmod temport labore et dolore magna"
    response = client.post(
        "api/v1/red-flags", headers=user1_header, data=json.dumps(new_record)
    )
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["data"][0]["message"] == "Created red-flag record"
    assert data["data"][0]["red-flag"]["id"] == 4
    assert data["data"][0]["red-flag"]["title"] == new_record['title']
    assert data["data"][0]["red-flag"]["comment"] == new_record['comment']
    assert data["data"][0]["red-flag"]["createdBy"] == user1_id




def test_create_a_duplicate_red_flag(client):
    response = client.post(
        "api/v1/red-flags", headers=user1_header, data=json.dumps(new_record)
    )
    assert response.status_code == 409
    data = json.loads(response.data.decode())
    assert data["error"] == "Red-flag record already exists"


def test_create_a_red_flag_without_wrong_input(client):
    wrong_input_1 = new_record

    new_record["location"] = ["jk", 180]
    response = client.post(
        "api/v1/red-flags", headers=user1_header, data=json.dumps(new_record)
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"]["location"] == "location coordinates must be a number"
    assert len(data["error"]) == 1

    wrong_input_1["title"] = "6"
    wrong_input_1["location"] = ""
    wrong_input_1["tags"] = ""
    wrong_input_1["Images"] = ""
    wrong_input_1["Videos"] = ""
    wrong_input_1["comment"] = "5"
    # create a red flag with one coordinate in the location
    response = client.post(
        "api/v1/red-flags",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )

    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"]["title"] == "Field cannot be a number"
    assert (
            data["error"]["location"]
            == "location must be a list with both Latitude and Longitude coordinates"
    )
    assert (
            data["error"]["tags"]
            == "Please provide a list of tags i.e ['crime','rape'] or an empty list"
    )
    assert (
            data["error"]["Images"]
            == "Please provide an empty list of Images if none"
    )
    assert (
            data["error"]["Videos"]
            == "Please provide an empty list of Videos if none"
    )
    assert data["error"]["comment"] == "Field cannot be a number"
    assert len(data["error"]) == 6

    wrong_input_1["title"] = "my"
    wrong_input_1["location"] = [-90, 180]
    wrong_input_1["tags"] = [12]
    wrong_input_1["Images"] = ["mine.png"]
    wrong_input_1["Videos"] = ["crime.mpeg"]
    wrong_input_1["comment"] = "Lorem ipsum"

    response = client.post(
        "api/v1/red-flags",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (
            data["error"]["title"]
            == "Field must contain a minimum of 4 characters"
    )
    assert (
            data["error"]["location"]
            == "latitude must be between -90 and 90 and longitude coordinates must be between -180 and 180"
    )
    assert (
            data["error"]["tags"]
            == "Tags must be of string type i.e ['crime','rape']"
    )
    assert data["error"]["Images"] == "Only JPEG Images are supported"
    assert data["error"]["Videos"] == "Only MP4 Videos are supported"
    assert len(data["error"]) == 5

    wrong_input_1["title"] = ""

    response = client.post(
        "api/v1/red-flags",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (
            data["error"]["title"]
            == "Field must contain a minimum of 4 characters"
    )

    wrong_input_1["title"] = (
        "orem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet massa"
        " in elit accumsan bibendum. Suspendisse tincidunt, justo quis laoreet elementum,"
        "enim ligula consectetur ligula, quis fringilla ligula augue non nibh. "
    )

    response = client.post(
        "api/v1/red-flags",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (
            data["error"]["title"]
            == "Field must contain a maximum of 100 characters"
    )
