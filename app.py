from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_bcrypt import Bcrypt
from database import db
from flask_marshmallow import Marshmallow

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
marshmallow = Marshmallow(app)
bcrypt = Bcrypt(app)
db.init_app(app)
