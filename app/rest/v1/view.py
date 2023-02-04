from . import rest_v1
from app.model import User, db, Permissions
from flask import jsonify, request
from ..errors import errors
from flasgger import swag_from


@rest_v1.route("/users", methods=['GET'])
@swag_from('swagger_schema/user_view/get_users.yml')
def get_users():
    try:
        users = User.query.all()
        list_users = [user.to_json() for user in users]
        return jsonify(list_users)

    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['GET'])
@swag_from('swagger_schema/user_view/get_user.yml')
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        return jsonify(user.to_json())
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users", methods=['POST'])
@swag_from('swagger_schema/user_view/post_user.yml')
def post_user():
    try:
        data = request.get_json()
        user = User.from_json(data)
        db.session.add(user)
        db.session.commit() # вернуть сохраненного пользователя в момент комита
        return jsonify(user.to_json())
    except AttributeError:
        return jsonify(errors.get('PasswordNotFound')), errors.get('PasswordNotFound').get('status')
    except KeyError:
        return jsonify(errors.get('PermissionNotFound')), errors.get('PermissionNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['PUT'])
@swag_from('swagger_schema/user_view/put_user.yml')
def put_user(id):
    try:
        data = request.get_json()
        user = User.query.filter_by(id=id).first()
        user.user_name = data.get('user_name') or user.user_name
        user.password = data.get('password') or user.password
        if data.get('permission'):
            user.permission = Permissions.__getitem__(data.get('permission'))
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_json())
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')


@rest_v1.route("/users/<int:id>", methods=['DELETE'])
@swag_from('swagger_schema/user_view/delete_user.yml')
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')
        db.session.delete(user)
        db.session.commit()
        return {'сообщение': 'пользователь удален'}
    except AttributeError:
        return jsonify(errors.get('UserNotFound')), errors.get('UserNotFound').get('status')
