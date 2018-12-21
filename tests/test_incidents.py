from flask import json
from .base import user1_header

comment = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""
empty_location =  {"location": " ","comment":comment}
valid_data =  {"location":"12.767 12.667" ,"comment":comment}


invalid_location =  {"location":"12212" ,"comment":comment}
with_no_comment=  {"location": "12.3 34.5"}

def test_create_a_red_flag(client):
    # test only logged in user can create red flag
    response = client.post("api/v1/red-flags")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {'message': "Invalid Token verification failed", 'status': 401}

    # create a red flag with no data
    response = client.post('api/v1/red-flags',headers=user1_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['error'] == "Provide provide valid data"



    # create a red flag with one coordinate in the location
    response = client.post("api/v1/red-flags",headers=user1_header,data=json.dumps(invalid_location))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['message'] == "location must contain both latitude and longitude"

    # create a red flag with coordinate containing a letter
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(invalid_location))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['message'] == "location must contain both latitude and longitude"


    # create a red flag with no_comment
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(with_no_comment))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['message'] == "Please provide a comment"

    # create a red flag with valid data
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(valid_data))
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['data']['comment'] == comment

    # create duplicate red flag
    response = client.post("api/v1/red-flags", headers=user1_header, data=json.dumps(valid_data))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['error'] == "Red-flag record already exists"