from flask import json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}
valid_user ={
        "firstname":"Micheal",
        "lastname":"Scott",
        "othernames":"Gerald",
        "email":"scottd@gmail.com",
        "phoneNumber": "0772019937",
        "username": "user9",
        "password":"Password123"
 }


def test_user_login_(client):
    "Tests login a user "
    # create user
    register_response =client.post('/api/v1/auth/register', data=json.dumps(valid_user), headers=headers)
    assert register_response.status_code == 201

    # with wrong credentials
    response= client.post('/api/v1/auth/login', data=json.dumps({"username": "usehr1", "password": "Password123"}),
        headers=headers)
    assert response.status_code == 401
    data= json.loads(response.data.decode())
    assert data['error']== 'Invalid credentials'

    # Tests login with correct credentials
    response= client.post('/api/v1/auth/login',
     data=json.dumps({"username": "user9", "password": "Password123"}),
     headers=headers)
    assert response.status_code ==200
    data= json.loads(response.data.decode())
    assert data['message']== 'Logged in successfully'


