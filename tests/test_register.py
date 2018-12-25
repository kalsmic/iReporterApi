from flask import json

from api.helpers.responses import (
    wrong_name,
    wrong_password,
    wrong_phone_number,
    duplicate_user_name,
    duplicate_email

)

mimetype = "application/json"
headers = {"Content-Type": mimetype, "Accept": mimetype}

new_user_data =  {
    "firstname":"3",
    "lastname":"John David",
    "email":"userOnehireporter.com",
    "phoneNumber":"07f73125678",
    "password":"password",
    "username":"ur1",
    "othernames":"4"
}
data_with_wrong_keys ={
                "firstname": "Arthur",
                "lastname": "kalule",
                "otherames": "Gerald",
                "email": "kalulearthur@gmail.com",
                "firstname": "Arthur",
                "lastname": "Kalule",
                "othernames": "Gerald",
                "phoneNumber": "0772019937",
                "username": "arthur",
            }

def test_register_with_no_data(client):
    response = client.post("api/v1/auth/register", headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Provide provide valid data to register"


def test_register_with_wrong_key(client):
    response = client.post("api/v1/auth/register", headers=headers, data=json.dumps(data_with_wrong_keys)  )
    assert response.status_code == 422
    data = json.loads(response.data.decode())
    assert data["error"] == "Please provide the correct keys for the data"
#
#
def test_register_with_wrong_invalid_format_data(client):

    response = client.post("api/v1/auth/register", headers=headers, data=json.dumps(new_user_data))
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert (data["error"]["firstname"] == wrong_name)
    assert (data["error"]["lastname"] == wrong_name)
    assert (data["error"]["othernames"] == wrong_name)
    assert (data["error"]["password"] == wrong_password)
    assert (data["error"]["phoneNumber"] == wrong_phone_number)

def test_register_with_wrong_valid_format_data(client):

    new_user_data["firstname"] = "John"
    new_user_data["lastname"] = "David"
    new_user_data["othernames"] = "Mark"
    new_user_data["username"] = "JDMark123"
    new_user_data["email"] = "jdmark@email.com"
    new_user_data["phoneNumber"] = "0772123123"
    new_user_data["password"] = "Password123"

    response = client.post("api/v1/auth/register", headers=headers, data=json.dumps(new_user_data))
    assert response.status_code == 201
    data = json.loads(response.data.decode())
    # assert data["data"]["email"] == "email@gmail.com"
    # assert data["data"]["is_admin"] == False
    assert data["data"][0]["message"]== "Account created Successfully"
    assert data["data"][0]["id"]== 4


def test_register_duplicate_user(client):

    response = client.post("api/v1/auth/register", headers=headers, data=json.dumps(new_user_data))
    assert response.status_code == 409
    data = json.loads(response.data.decode())
    assert data["error"] == duplicate_email

    new_user_data["email"] = "jdmark2@email.com"
    response = client.post("api/v1/auth/register", headers=headers, data=json.dumps(new_user_data))
    assert response.status_code == 409
    data = json.loads(response.data.decode())
    assert data["error"] == duplicate_user_name
