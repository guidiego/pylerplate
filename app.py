from flask import Flask, request
from flask_apispec import FlaskApiSpec
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_redis import FlaskRedis
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from database import db
from utils.openapi import register_rules
from utils.error_handlers import (
    BaseError, internal_server_handler,
    handle_marshmallow_error, db_integrity_error
)

marshmallow = Marshmallow()
bcrypt = Bcrypt()
auth_token_db = FlaskRedis()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.update({
        'APISPEC_TITLE': 'Pylerplate',
        'APISPEC_VERSION': 'Pylerplate',
        'APISPEC_SWAGGER_URL': '/swagger/',
        'APISPEC_SWAGGER_UI_URL': None,
    })

    app.__docs__ = FlaskApiSpec(app)
    initialize_extensions(app)
    register_handlers(app)
    CORS(app)

    register_routes(app)

    return app


def initialize_extensions(app):
    db.init_app(app)
    marshmallow.init_app(app)
    bcrypt.init_app(app)
    auth_token_db.init_app(app)


def register_handlers(app):
    app.register_error_handler(BaseError, BaseError.handle_error)
    app.register_error_handler(ValidationError, handle_marshmallow_error)
    app.register_error_handler(500, internal_server_handler)
    app.register_error_handler(IntegrityError, db_integrity_error)


def register_routes(app):
    from modules.auth.api import AuthResource
    from modules.user.api import UserResource

    register_rules(app, [
        AuthResource,
        UserResource
    ])

    @app.after_request
    def access_log(response):
        if app.config['FLASK_ENV'] != 'development':
            data = {
                'user': 'None',
                'method': request.method,
                'url': request.path,
                'status_code': response.status_code,
            }

            if hasattr(request, 'context'):
                data['user'] = request.context.user.id

            print(
                '[AccessInfo] Method: {method} | Path: {url} | StatusCode: {status_code} | User<{user}>'.format(**data),
                flush=True
            )

        return response

    @app.route('/', methods=['GET'])
    def health_check():
        return "Don't panic! We're okey!"