from flask import json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

valid_user ={
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"kalule@gmail.com",
        "phoneNumber": "0772019937",
        "username": "kalsmic",
        "password":"Password123"
    }
duplicate_username ={
    "firstname":"arthur",
    "lastname":"kalule",
    "othernames":"Gerald",
    "email":"kaluse@gmail.com",
    "phoneNumber": "0772019937",
    "username": "kalsmic",
    "password":"Password123"
}
duplicate_email ={
    "firstname":"arthur",
    "lastname":"kalule",
    "othernames":"Gerald",
    "email":"kalule@gmail.com",
    "phoneNumber": "0772019937",
    "username": "Nelson",
    "password":"Password123"
}

def test_register_with_no_data(client):
    response = client.post('api/v1/auth/register',headers=headers)
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] == 'Please provide valid data'


def test_register_with_wrong_key(client):
    """test register with wrong key in data"""
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"Arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"kalulearthur@gmail.com",
        "firstname": "Arthur",
        "lastname": "Kalule",
        "othernames":"Gerald",
        "phoneNumber": "0772019937",
        "username": "arthur"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] == "Please provide the correct keys for the data"

def test_register_with_invalid_or_missing(client):
    """test register with missing or invalid"""
    # blank first name
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"kalulearthur@gmail.com",
        "phoneNumber": "0772019937",
        "username": "arthur",
        "password":"Password123"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] ==f"""Name fields cannot be empty or contain any space or number character"""

    # number in lastname
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"k5alule",
        "othernames":"Gerald",
        "email":"kalulearthur@gmail.com",
        "phoneNumber": "0772019937",
        "username": "arthur",
        "password":"Password123"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] ==f"""Name fields cannot be empty or contain any space or number character"""

    # no username
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"kalulearthur@gmail.com",
        "phoneNumber": "0772019937",
        "username": "",
        "password":"Password123"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] ==f"""username cannot be empty or contain any a space in it"""

    # wrong email
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"@gmail.com",
        "phoneNumber": "0772019937",
        "username": "username",
        "password":"Password123"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] ==f"""please provide a valid email"""


    # test phonenumber with characters in it
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"email@gmail.com",
        "phoneNumber": "0u72019937",
        "username": "username",
        "password":"Password123"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] ==f"phoneNumber must be a string of ten numbers only"

# test password has less than 8 characters 
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"email@gmail.com",
        "phoneNumber": "0772019937",
        "username": "username",
        "password":""
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] =="Password Must contain a Minimum 8 characters."

    # test password combination 
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"email@gmail.com",
        "phoneNumber": "0772019937",
        "username": "username",
        "password":"uhhjhhjj"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] == "Password must contain atleast one upper case letter"

    # test password is a combination of letters and numbers
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"email@gmail.com",
        "phoneNumber": "0772019937",
        "username": "username",
        "password":"Passssword"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] =="Password must contain atleast one number"

    # test password contains lower case letter
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"email@gmail.com",
        "phoneNumber": "0772019937",
        "username": "username",
        "password":"PASSWORD1223"
    }))
    assert response.status_code == 400
    data= json.loads(response.data.decode()) 
    assert data['error'] =="Password must contain atleast lower case letter"

    # test register user with correct data
def test_register_with_valid(client):
  
    response = client.post('api/v1/auth/register',headers=headers,
    data=json.dumps( {
        "firstname":"arthur",
        "lastname":"kalule",
        "othernames":"Gerald",
        "email":"kalule@gmail.com",
        "phoneNumber": "0772019937",
        "username": "kalsmic",
        "password":"Password123"
    }))
    assert response.status_code ==201
    data= json.loads(response.data.decode()) 
    assert data['data']['email'] == "kalule@gmail.com"
    assert data['data']['isAdmin'] == False
    assert data['data']['phoneNumber'] == "0772019937"

 # test register user 
def test_register_with_duplicate_user(client):
  
    response = client.post('api/v1/auth/register',headers=headers,
     data=json.dumps( duplicate_username))
    assert response.status_code ==403
    data= json.loads(response.data.decode()) 
    assert data['error']== 'Username already taken'
    response = client.post('api/v1/auth/register',headers=headers,
     data=json.dumps( duplicate_email))
    assert response.status_code ==403
    data= json.loads(response.data.decode()) 
    assert data['error']== "Email address exists"

