from . import rest_v1
from app.model import User, db, Permissions
from flask import jsonify, request
from ..errors import errors
from flasgger import swag_from
from flask_login import login_user, logout_user, login_required
from ... import login_manager
from ...registration_login_entity import RegistrationLoginEntity
from ...repository.user_query_repository import user_query_filter, user_query_odrer_by

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#
@rest_v1.route('/registration', methods=['POST'])
def registration():
    email, password = RegistrationLoginEntity.request_json()
    if RegistrationLoginEntity.email_password_validate(email, password) is False:
        abort(400)
    if user_query_filter(email=email) is not None:
            abort(400, description='Пользователь с данным email и password зарегистирован')
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'email': user.email}), 201

@rest_v1.route('/login', methods=['POST'])
def login():
    email, password = RegistrationLoginEntity.request_json()
    if RegistrationLoginEntity.email_password_validate(email, password) is False:
        abort(400)
    user = user_query_filter(email=email)
    if RegistrationLoginEntity.user_check_password_validate(user, password) is True:
    # login_user(user, remember=True)
    # token = create_token(user=user, secret_key=app.config['SECRET_KEY'])
    # add_token(token, user)
    # return jsonify({'email': user.email, 'token': token}), 201
        return jsonify(user.to_json()), 201


@rest_v1.route("/users", methods=['GET'])
@swag_from('swagger_schema/user_view/get_users.yml')
def get_users():
    try:
        users = user_query_odrer_by(User.id)
        list_users = [user.to_json() for user in users]
        return jsonify(list_users)

    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['GET'])
@swag_from('swagger_schema/user_view/get_user.yml')
def get_user(id):
    try:
        user = user_query_filter(id=id)
        return jsonify(user.to_json())
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


# @rest_v1.route("/users", methods=['POST'])
# @swag_from('swagger_schema/user_view/post_user.yml')
# def post_user():
#     try:
#         data = request.get_json()
#         user = User.from_json(data)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify(user.to_json())
#     except AttributeError:
#         return jsonify(errors.get('PasswordNotFound')), errors.get('PasswordNotFound').get('status')
#     except KeyError:
#         return jsonify(errors.get('PermissionNotFound')), errors.get('PermissionNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['PUT'])
@swag_from('swagger_schema/user_view/put_user.yml')
def put_user(id):
    try:
        email, password = RegistrationLoginEntity.request_json()
        user = user_query_filter(id=id)
        user.email = email or user.email
        user.password = password or user.password
        permission = RegistrationLoginEntity.request_json_put()
        if permission:
            user.permission = permission
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_json())
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['DELETE'])
@swag_from('swagger_schema/user_view/delete_user.yml')
def delete_user(id):
    try:
        user = user_query_filter(id=id)
        if not user:
            return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')
        db.session.delete(user)
        db.session.commit()
        return {'сообщение': 'пользователь удален'}
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')
