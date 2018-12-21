from flask import json
from api.helpers import encode_token
from api.models.user import users, User

user1 = User(firstname='Micheal',lastname='kan',othernames='Omoding',email='user1@email.com',
             phoneNumber='07731235678',password='Password123', username='user1')
user1_id = user1.id
users.append(user1)

def generate_token(id):
    token = encode_token(id)
    mimetype = 'application/json'

    headers = {
        'Content-Type': mimetype,
        'Authorization': 'Bearer ' + token
    }
    return headers
user1_header = generate_token(user1_id)
# admin_header = generate_token(users[0])

