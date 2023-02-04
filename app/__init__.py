from flask import Flask
from config import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()
moment = Moment()

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    migrate.init_app(app, db)
    db.init_app(app)
    swagger.init_app(app)
    moment.init_app(app)

    from app.rest.v1 import rest_v1
    csrf.exempt(rest_v1)
    app.register_blueprint(rest_v1)

    return app