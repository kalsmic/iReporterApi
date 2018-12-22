from flask import json
from api.app import create_app
from api.helpers import decode_token

app = create_app({'TESTING': True})
client = app.test_client()

admin_response = client.post('/api/v1/auth/login', data=json.dumps({"username": "admin", "password": "Password123"}))
admin_token = json.loads(admin_response.data.decode())["token"]
mimetype = 'application/json'

admin_header = {
    'Content-Type': mimetype,
    'Authorization': 'Bearer ' + admin_token
}

user1_response = client.post('/api/v1/auth/login',
                             data=json.dumps({"username": "user1", "password": "Password123"}))
user1_token = json.loads(user1_response.data.decode())["token"]

user1_header = {
    'Content-Type': mimetype,
    'Authorization': 'Bearer ' + user1_token
}

user2_response = client.post('/api/v1/auth/login',
                             data=json.dumps({"username": "user2", "password": "Password123"}))
user2_token = json.loads(user1_response.data.decode())["token"]

user2_header = {
    'Content-Type': mimetype,
    'Authorization': 'Bearer ' + user2_token
}

admin_user_id = decode_token(admin_token)['userid']
user1_id = decode_token(user1_token)['userid']
user2_id = decode_token(user2_token)['userid']
client.post("api/v1/red-flags",
            headers=user1_header,
            data=json.dumps({"location": "12.767 277", "comment": "my first red flag incident"}))
