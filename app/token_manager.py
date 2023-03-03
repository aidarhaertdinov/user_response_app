import itsdangerous
from itsdangerous import TimedSerializer
import base64
from flask import abort, current_app


def create_token(user, secret_key: str) -> str:
    s = TimedSerializer(secret_key)
    str_payload = s.dumps({
        'id': user.id,
        'email': user.email
    })
    token = base64.b64encode(str_payload.encode('ascii'))

    return token.decode('ascii')


def add_token(token: str, current_user) -> dict:
    current_app.config[current_user.id] = token

    return current_app.config


def decode_token(token, secret_key):

    try:
        s = TimedSerializer(secret_key)
        data = s.loads(decoder(token), max_age=1)
        return data

    except itsdangerous.exc.SignatureExpired:
        delete_token(token)
        abort(400, description='Срок действия подписи истек. Пожалуйста, войдите в систему еще раз')


def delete_token(token):
    for key, value in current_app.config.items():
        if value == token:
            del current_app.config[key]
            break

    return current_app.config


def decoder(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    return message
