import os

from flask import Flask
from flask_jwt_extended import JWTManager

from instance.config import config
from app.api.v2.database import init_db

jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', default='SdaHv342nx!jknr837bjwd?c,lsajjjhw673hdsbgeh')
    init_db()

    jwt.init_app(app)

    from .api.v2 import endpoint_v2_blueprint as v2_blueprint
    app.register_blueprint(v2_blueprint, url_prefix='/api/v2')

    from .api.v2 import auth_v2_blueprint as v2_blueprint
    app.register_blueprint(v2_blueprint, url_prefix='/api/v2/auth')

    return app
