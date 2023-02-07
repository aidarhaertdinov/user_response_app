from flask import Flask
from config import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()
moment = Moment()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    migrate.init_app(app, db)
    db.init_app(app)
    swagger.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from app.rest.v1 import rest_v1
    csrf.exempt(rest_v1)
    app.register_blueprint(rest_v1)

    return app