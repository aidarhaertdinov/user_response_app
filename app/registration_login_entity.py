from flask import request

class RegistrationLoginEntity:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def request_json():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        return email, password

    @staticmethod
    def request_json_put():
        data = request.get_json()
        permission = data.get('permission')
        if permission:
            return permission
        else:
            return False


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
