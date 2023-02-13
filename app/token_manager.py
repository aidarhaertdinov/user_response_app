
import jwt
from datetime import datetime, timedelta

from flask import abort



dict_token = {}


def create_token(user, secret_key: str) -> str:
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(days=10)
    }, secret_key, algorithm='HS256')

    return token


def add_token(token: str, current_user) -> dict:
    global dict_token
    dict_token[current_user.id] = token

    return dict_token


def decode_token(token, secret_key):
    try:
        data = jwt.decode(token, secret_key, algorithms='HS256')
        return data
    except jwt.ExpiredSignatureError:
        delete_token(token)
        abort(400, description='Срок действия подписи истек. Пожалуйста, войдите в систему еще раз')


# def delete_token(token):
#     global dict_token
#     for key, value in dict_token.items():
#         if value == token:
#             del dict_token[key]
#             break
#     return dict_token

def delete_token(token):
    global dict_token
    try:
        list(dict_token.values()).remove(token)
        return True
    except ValueError:
        return False


