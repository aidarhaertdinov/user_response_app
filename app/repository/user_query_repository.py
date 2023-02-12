from app.model import User


def user_query_filter(**kwargs: dict) -> User:
    return User.query.filter_by(**kwargs).first()


def user_query_odrer_by(*args: str) -> User:
    return User.query.order_by(*args).all()