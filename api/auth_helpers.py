import jwt
import datetime
from functools import wraps
from os import environ

from flask import request,jsonify
secret_key = environ.get("SECRET_KEY")


def encode_token(user_id):
    token = jwt.encode({
    'userid':str(user_id),
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    }, secret_key).decode('utf-8') 
    return token

def decode_token(token):

     dc = jwt.decode(token, secret_key, algorithm='HS256')
     return dc

def token_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers['token']
            try:
                decode_token(token)

                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"message":"token expired"}),401
            except jwt.InvalidTokenError:
                return jsonify({"message":"Invalid Token verification failed"}),401
        except KeyError:
            return jsonify({"message":"Missing token"}),401

    return wrapper