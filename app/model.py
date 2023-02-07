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
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.Text)
    username = db.Column(db.String(20))
    permission = db.Column(db.Enum(Permissions))
    created_date = db.Column(db.DateTime(timezone=True), nullable=False)


    def __init__(self, email, password, username=None, permission=Permissions.USER):
        self.email = email
        self.username = username
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
                'email': self.email,
                'username': self.username,
                'permission': self.permission.value}

    @staticmethod
    def from_json(_dict: dict):
        return User(email=_dict.get('email'),
                    username=_dict.get('username'),
                    password=_dict.get('password'),
                    permission=Permissions.__getitem__(_dict.get('permission')))


@event.listens_for(User, "before_insert")
def add_created_date(mapper, connection, target):
    target.created_date = moment.create(datetime.utcnow()).timestamp
@event.listens_for(User, "before_insert")
def lowercase(mapper, connection, target):
    target.email = target.email.lower()

