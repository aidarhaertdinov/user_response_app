
import jwt
from datetime import datetime, timedelta

from flask import abort, current_app



# dict_token = {}


def create_token(user, secret_key: str) -> str:
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(days=10)
    }, secret_key, algorithm='HS256')

    return token


def add_token(token: str, current_user) -> dict:
    current_app.config[current_user.id] = token
    return current_app.config


def decode_token(token, secret_key):
    try:
        data = jwt.decode(token, secret_key, algorithms='HS256')
        return data
    except jwt.ExpiredSignatureError:
        delete_token(token)
        abort(400, description='Срок действия подписи истек. Пожалуйста, войдите в систему еще раз')


def delete_token(token):
    for key, value in current_app.config.items():
        if value == token:
            del current_app.config[key]
            break
    return current_app.config

# TODO метод не рабочий
# def delete_token(token):
#     try:
#         list(current_app.config.values()).remove(token)
#         return True
#     except ValueError:
#         return False


