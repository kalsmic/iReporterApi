from flask import json

from api.helpers.responses import wrong_description
from .base import admin_header, user2_header, user1_header
from api.models.incident import red_flags
new_record = {
        "title":"My First red flag",
        "description":"Lorem ipsum eiusmod temport labore et dolore magna",
        "location": [-80,-174.4],
        "tags": ["crime","rape"],
        "Images":["image1.jpg","image2.jpg"],
        "Videos":["vid1.mp4","vid2.mp4"],
        "comment":"Lorem ipsum dolor sit amet, consectetur adipiscing"
 }

def test_create_a_red_flag_without_a_token(client):
    # test only logged in user with token
    response = client.post("api/v1/red-flags")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {
        "error": "Invalid Token verification failed",
        "status": 401,
    }

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
    response = client.post("api/v1/red-flags", headers=user1_header,data=json.dumps(new_record))
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    assert data["data"][0]["message"] == "Created red-flag record"
    assert data["data"][0]["id"] == 1

def test_create_a_duplicate_red_flag(client):
    response = client.post("api/v1/red-flags", headers=user1_header,data=json.dumps(new_record))
    assert response.status_code == 409
    data = json.loads(response.data.decode())
    assert data["error"] == "Red-flag record already exists"

def test_create_a_red_flag_without_wrong_input(client):

    wrong_input_1 = new_record

    new_record["location"] = ["jk", 180]
    response = client.post(
        "api/v1/red-flags",
        headers=user1_header,
        data=json.dumps(new_record),
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (data["error"]["location"] == "location coordinates must be a number")
    assert (len(data["error"]) == 1)

    wrong_input_1["title"] ="6"
    wrong_input_1["description"] =""
    wrong_input_1["location"] =""
    wrong_input_1["tags"] =""
    wrong_input_1["Images"] =""
    wrong_input_1["Videos"] =""
    wrong_input_1["comment"] ="5"
    # create a red flag with one coordinate in the location
    response = client.post(
        "api/v1/red-flags",
        headers=user1_header,
        data=json.dumps(wrong_input_1),
    )

    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert ( data["error"]["title"] == "Field cannot be a number")
    assert ( data["error"]["description"] == wrong_description )
    assert ( data["error"]["location"] == "location must be a list with both Latitude and Longitude coordinates" )
    assert ( data["error"]["tags"] == "Please provide a list of tags i.e ['crime','rape'] or an empty list")
    assert ( data["error"]["Images"] == "Please provide an empty list of Images if none")
    assert ( data["error"]["Videos"] ==  "Please provide an empty list of Videos if none")
    assert ( data["error"]["comment"] ==  "Comment must be a string" )
    assert (len(data["error"]) == 7)

    wrong_input_1["title"] = "my"
    wrong_input_1["description"] = "23"
    wrong_input_1["location"] = [-90, 180]
    wrong_input_1["tags"] = [12]
    wrong_input_1["Images"] = ["mine.png"]
    wrong_input_1["Videos"] = ["crime.mpeg"]
    wrong_input_1["comment"] = "Lorem ipsum"

    response = client.post("api/v1/red-flags",headers=user1_header, data=json.dumps(wrong_input_1),)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (data["error"]["title"] == "Field must contain a minimum of 4 characters")
    assert (data["error"]["description"] == "Please provide a description of type string")
    assert (data["error"]["location"] == "latitude must be between -90 and 90 and longitude coordinates must be between -180 and 180")
    assert (data["error"]["tags"] == "Tags must be of string type i.e ['crime','rape']")
    assert (data["error"]["Images"] == "Only JPEG Images are supported")
    assert (data["error"]["Videos"] == "Only MP4 Videos are supported")
    assert (len(data["error"]) == 6)

    wrong_input_1["title"] = ""

    response = client.post("api/v1/red-flags",headers=user1_header,data=json.dumps(wrong_input_1), )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (data["error"]["title"] == "Field cannot be blank")

def test_get_all_red_flags_withour_token(client):
    # test only logged in user get red flags
    response = client.get("api/v1/red-flags")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {
        "error": "Invalid Token verification failed",
        "status": 401,
    }

def test_get_all_red_flags(client):
    response = client.get("api/v1/red-flags", headers=user2_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"][0]["createdBy"] == 2

def test_get_a_red_flag_which_does_not_exist(client):
    response = client.get("api/v1/red-flags/12", headers=user2_header)
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["error"] == "Red-flag record does not exist"

def test_get_a_red_flag(client):
    response = client.get("api/v1/red-flags/1", headers=user2_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0][0]["Images"] == ['image1.jpg', 'image2.jpg']
    assert data["data"][0][0]["comments"][0]["body"] == "Lorem ipsum dolor sit amet, consectetur adipiscing"
    assert data["data"][0][0]["comments"][0]["commentBy"] == 1

def test_get_a_red_flag_with_invalid_id(client):
    response = client.get("api/v1/red-flags/fs", headers=user2_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Red-flag id must be an integer"

def test_edit_a_red_flag_location_without_a_token(client):
    response = client.patch("api/v1/red-flags/1/location")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["status"] == 401
    assert data["error"] == "Invalid Token verification failed"

def test_edit_a_red_flag_location_which_does_not_exist(client):
    response = client.patch("api/v1/red-flags/12/location",headers=user1_header,data=json.dumps({"location": [12,12]}))
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["status"] == 404
    assert data["error"] == "Red-flag record does not exist"

def test_edit_a_red_flag_location_which_does_not_belong_to_user(client):
    response = client.patch("api/v1/red-flags/1/location",headers=user2_header,data=json.dumps({"location": [12,12]}))
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You're not allowed to modify this resource"

def test_edit_a_red_flag_location_with_invalir_red_flag_id(client):
    response = client.patch("api/v1/red-flags/df/location",headers=user2_header,data=json.dumps({"location": [12,12]}))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Red-flag id must be an number"

def test_edit_a_red_flag_location_status_of_draft(client):
    response = client.patch("api/v1/red-flags/1/location",headers=user1_header,data=json.dumps({"location": [12,12]}))
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0]["message"] == "Updated red-flag record’s location"
    assert data["data"][0]["id"] == 1

def test_edit_a_red_flag_location_with_invalid_location_coordinates(client):
    response = client.patch("api/v1/red-flags/1/location",headers=user1_header,data=json.dumps({"location": [-90,12]}))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] ==  "latitude must be between -90 and 90 and longitude coordinates must be between -180 and 180"

def test_edit_a_red_flag_location_status_other_than_draft(client):
    red_flags[0].status = "under investigation"
    response = client.patch("api/v1/red-flags/1/location",headers=user1_header,data=json.dumps({"location": [12,12]}))
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert data["status"] == 403
    assert data["error"] == "You're not allowed to modify this resource"
