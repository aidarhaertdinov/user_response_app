from . import rest_v1
from app.model import User, db
from flask import jsonify
from ..errors import errors
from flasgger import swag_from
from app.auth.registration_login_entity import RegistrationLoginEntity
from ...repository.user_repository import UserRepository
from app import multi_auth


@rest_v1.route('/create_user', methods=['POST'])
def create_user():
    data = RegistrationLoginEntity.request_json()
    if RegistrationLoginEntity.email_password_validate(data.email, data.password) is False:
        abort(400)
    if UserRepository.get_user_by_email(email=data.email) is not None:
            abort(400, description='Пользователь с данным email и password зарегистирован')
    user = User(email=data.email, password=data.password, username=data.username, permission=data.permission )
    db.session.add(user)
    db.session.commit()
    return jsonify({'email': user.email}), 201

@rest_v1.route("/users", methods=['GET'])
@multi_auth.login_required
@swag_from('swagger_schema/user_view/get_users.yml')
def get_users():
    try:
        users = UserRepository.get_ordered_users(User.id)
        list_users = [user.to_json() for user in users]
        return jsonify(list_users)

    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['GET'])
@multi_auth.login_required
@swag_from('swagger_schema/user_view/get_user.yml')
def get_user(id):
    try:
        user = UserRepository.get_user_by_id(id=id)
        return jsonify(user.to_json())
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['PUT'])
@multi_auth.login_required
@swag_from('swagger_schema/user_view/put_user.yml')
def put_user(id):
    try:
        data = RegistrationLoginEntity.request_json()
        user = UserRepository.get_user_by_id(id=id)
        user.email = data.email or user.email
        user.password_hash = data.password or user.password_hash
        if data.permission:
            user.permission = data.permission
        if data.username:
            user.username = data.username
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_json())
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['DELETE'])
@multi_auth.login_required
@swag_from('swagger_schema/user_view/delete_user.yml')
def delete_user(id):
    try:
        user = UserRepository.get_user_by_id(id=id)
        if not user:
            return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')
        db.session.delete(user)
        db.session.commit()
        return {'сообщение': 'пользователь удален'}
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')
