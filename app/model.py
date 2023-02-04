from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from app import db, moment
from sqlalchemy import event
from datetime import datetime


class Permissions(Enum):
    MODERATE = "MODERATE"
    ADMIN = "ADMIN"
    USER = "USER"


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(70), unique=True)
    password = db.Column(db.Text)
    permission = db.Column(db.Enum(Permissions))
    created_date = db.Column(db.DateTime(timezone=True), nullable=False)


    def __init__(self, name, password, permission=Permissions.USER):
        self.user_name = name
        self.hash_password(password)
        self.permission = permission

    def __repr__(self):
        return '<User %r>' % self.id

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def can(self, perm):
        return self.permission is not None and self.permission == perm

    def to_json(self):
        return {'id': self.id,
                'user_name': self.user_name,
                'permission': self.permission.value}

    @staticmethod
    def from_json(_dict: dict):
        return User(name=_dict.get('user_name'),
                    password=_dict.get('password'),
                    permission=Permissions.__getitem__(_dict.get('permission')))


@event.listens_for(User, "before_insert")
def add_created_date(mapper, connection, target):
    target.created_date = moment.create(datetime.utcnow()).timestamp
@event.listens_for(User, "before_insert")
def lowercase(mapper, connection, target):
    target.user_name = target.user_name.lower()

