from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.__docs__ = FlaskApiSpec(app)

bcrypt = Bcrypt(app)