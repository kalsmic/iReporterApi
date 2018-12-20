from flask import json


def test_index(client):
    "test if default shows welcome message"
    with client.get('/') as response:
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        expected = "Welcome to iReporter"
        assert data['welcome'] == expected

