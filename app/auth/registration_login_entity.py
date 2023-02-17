from flask import request

class RegistrationLoginEntity:

    def __init__(self, email, password, username, permission):
        self.email = email
        self.password = password
        self.username = username
        self.permission = permission

    @staticmethod
    def request_json():
        user = request.get_json()
        email = user.get('email')
        password = user.get('password')
        username = user.get('username')
        permission = user.get('permission')

        return RegistrationLoginEntity(email, password, username, permission)

    @staticmethod
    def email_password_validate(email: str, password: str) -> bool:
        if email is None or password is None:
            return False
        else:
            return True

    @staticmethod
    def user_check_password_validate(user: str, password: str) -> bool:
        if user is not None and user.verify_password(password):
            return True
        else:
            return False
