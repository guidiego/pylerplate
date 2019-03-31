from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_bcrypt import Bcrypt
from database import db
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.__docs__ = FlaskApiSpec(app)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

marshmallow = Marshmallow(app)
bcrypt = Bcrypt(app)
db.init_app(app)
