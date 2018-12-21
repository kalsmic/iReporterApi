from flask import json
from api.helpers import encode_token
from api.models.user import users, User

user1 = User(firstname='Micheal',lastname='kan',othernames='Omoding',email='user1@email.com',
             phoneNumber='07731245678',password='Password123', username='user1')
user2 = User(firstname='Joan',lastname='Atim',othernames='Keira',email='user2@email.com',
             phoneNumber='07731354678',password='Password123', username='user2')
user3 = User(firstname='Micheal',lastname='kan',othernames='Omoding',email='user1@email.com',
             phoneNumber='077312940678',password='Password123', username='user3')
user1_id = user1.id
user2_id = user2.id
user3_id = user3.id

users.extend([user1,user2,user3])


def generate_token(id):
    token = encode_token(id)
    mimetype = 'application/json'

    headers = {
        'Content-Type': mimetype,
        'Authorization': 'Bearer ' + token
    }
    return headers
user1_header = generate_token(user1_id)
user2_header = generate_token(user2_id)
user3_header = generate_token(user3_id)
# admin_header = generate_token(users[0])

