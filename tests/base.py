from flask import json

from api.app import create_app

app = create_app({"TESTING": True})
client = app.test_client()

admin_response = client.post(
    "/api/v1/auth/login",
    data=json.dumps({"username": "admin", "password": "Password123"}),
)
admin_token = json.loads(admin_response.data.decode())["token"]
mimetype = "application/json"

admin_header = {
    "Content-Type": mimetype,
    "Authorization": "Bearer " + admin_token,
}
admin_user_id = 1

user1_data = {
    "firstname": "userOne",
    "lastname": "userone",
    "email": "userOne@ireporter.com",
    "phoneNumber": "0773125678",
    "password": "Password123",
    "username": "user1",
    "othernames": "",
}
user2_data = {
    "firstname": "userTwo",
    "lastname": "lastTwo",
    "email": "usertwo@ireporter.com",
    "phoneNumber": "0774551567",
    "password": "Password123",
    "username": "user2",
    "othernames": "",
}

user1_response = client.post(
    "/api/v1/auth/register", data=json.dumps(user1_data)
)
data = json.loads(user1_response.data.decode())
user1_id = data["data"][0]["id"]

user2_response = client.post(
    "/api/v1/auth/register", data=json.dumps(user2_data)
)
data = json.loads(user2_response.data.decode())
user2_id = data["data"][0]["id"]

user1_response = client.post(
    "/api/v1/auth/login",
    data=json.dumps({"username": "user1", "password": "Password123"}),
)
user1_token = json.loads(user1_response.data.decode())["token"]

user2_response = client.post(
    "/api/v1/auth/login",
    data=json.dumps({"username": "user2", "password": "Password123"}),
)
user2_token = json.loads(user2_response.data.decode())["token"]

user1_header = {
    "Content-Type": mimetype,
    "Authorization": "Bearer " + user1_token,
}

user2_header = {
    "Content-Type": mimetype,
    "Authorization": "Bearer " + user2_token,
}
