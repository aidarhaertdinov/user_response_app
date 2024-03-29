from . import auth
from flask import jsonify, current_app, abort
from app.auth.model import RegistrationLoginEntity
from ..repository.user_repository import UserRepository
from app import basic_auth, token_auth


@basic_auth.verify_password
def verify_password(email, password):
    user = UserRepository.get_user_by_email(email=email)
    if not user or not user.verify_password(password):
        return False

    return user.email


from ..token_manager import create_token, add_token, decode_token


@token_auth.verify_token
def verify_token(token):
    data = decode_token(token=token, secret_key=current_app.config.get('SECRET_KEY'))
    if data['id'] in current_app.config:
        user = UserRepository.get_user_by_id(id=data['id'])
        return user

    return False


@auth.route('/login', methods=['POST'])
def login():
    data = RegistrationLoginEntity.request_json()
    if RegistrationLoginEntity.email_password_validate(data.email, data.password) is False:
        abort(400)
    user = UserRepository.get_user_by_email(email=data.email)
    if RegistrationLoginEntity.user_check_password_validate(user, data.password) is False:
        abort(400)
    token = create_token(user=user, secret_key=current_app.config.get('SECRET_KEY'))
    add_token(token, user)

    return jsonify({'id': user.id, 'token': token}), 201
