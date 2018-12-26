from flask import json
from api.helpers.responses import supported_end_points
def test_invalid_url(client):
    response = client.delete("api/v1/")
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["supportedEndPoints"] == supported_end_points
    assert data["error"] == "Endpoint for specified URL does not exist"

expired_token =  ("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
                  ".eyJ1c2VyaWQiOjEsImlzQWRtaW4iOjEsImlhdCI6MTU0NTgzNDA3NC"
                  "wiZXhwIjoxNTQ1ODM0MDc3fQ.a8yEOfyaJ6qUYbJJUmx-r9lPJ3jY"
                  "qIQK2_rqpJPGXFk"
                  )
wrong_signature = (
"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOjEsImlzQWRtaW4iOjEsImlhdCI6"
"MTU0NTgzNDQ5NywiZXhwIjoxNTQ1ODQ1Mjk3fQ.eUlRxwl-QDjBH4lnw_8mFJ78xpI1cD5QpOolw"
"oWP_vI"
)


expired_token_header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + expired_token,
}
invalid_token = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "ddd",
}

def test_expired_token(client):
    response = client.get("api/v1/red-flags",headers=expired_token_header)
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["error"] == "Signature has expired"

def test_invalid_token(client):
    response = client.get("api/v1/red-flags",headers=invalid_token)
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data["error"] == "Missing access token in header"
