from app.model import User


class UserRepository:

    def get_user_by_id(id: int) -> User:
        return User.query.filter_by(id=id).first()


    def get_user_by_email(email: str) -> User:
        return User.query.filter_by(email=email).first()


    def get_ordered_users(arg: str) -> list[User]:
        return User.query.order_by(arg).all()
