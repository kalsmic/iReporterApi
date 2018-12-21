import datetime
from functools import wraps
from os import environ

import jwt
from flask import request, jsonify

secret_key = environ.get('SECRET_KEY', 'my_secret_key')


def encode_token(user_id):

    payload = {
        'userid': user_id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')

    return token


def decode_token(token):

    decoded = jwt.decode(str(token), secret_key, algorithm='HS256')
    return decoded


def extract_token_from_header():
    authorizaton_header = request.headers.get("Authorization")
    if not authorizaton_header or 'Bearer' not in authorizaton_header:
        return jsonify({"message": "Bad authorization header", "status": 400}), 400
    token = str(authorizaton_header).split(' ')[1]
    return token


def token_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = extract_token_from_header()
            decode_token(token)
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Signature has expired", "status": 401}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid Token verification failed", "status": 401}), 401

    return wrapper


def request_data_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.data:
            return jsonify({
                'error': "Provide provide valid data",
                "status": 400
            }), 400
        return func(*args, **kwargs)

    return wrapper

def get_current_identity():
    return decode_token(extract_token_from_header())['userid']


if __name__ == "__main__":
    token = encode_token(1)
    print("Bearer " + str(token))
    print(token)
    print(decode_token(str(token)))