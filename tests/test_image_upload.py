from flask import json
import os
from .base import user1_header, admin_header
from werkzeug.datastructures import FileStorage



# Add image to red-flag record
def test_add_an_image_without_image_file(client):

    response = client.patch(
        "api/v2/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/addImage",
        headers=user1_header,

        )

    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Please provide an image file"

# Add image to red-flag record
def test_add_an_unsupported_image_type(client):
   with open(os.path.join('./tests/media/backer.txt'), 'rb') as fp:
        file = FileStorage(fp)
        response = client.patch(
            "api/v2/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/addImage",
            headers=user1_header,
            data={'image' : file}
            ,content_type='multipart/form-data'
            )

        assert response.status_code == 400
        data = json.loads(response.data.decode())
        assert data["status"] == 400
        assert data["error"] == "Only Image files of type {'png', 'jpeg', 'jpg', 'gif'} are supported"



# Add image to red-flag record
def test_add_an_image_to_a_red_flag_without_image(client):
   with open(os.path.join('./tests/media/test_image.gif'), 'rb') as fp:
        file = FileStorage(fp)
        response = client.patch(
            "api/v2/red-flags/10df0c67-5f2b-4e5d-8b45-7357bbf3bebb/addImage",
            headers=user1_header,
            data={'image' : file}
            ,content_type='multipart/form-data'
            )

        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert data["status"] == 200
        assert data["data"][0]["success"] == "Image added to red-flag record"