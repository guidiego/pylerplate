from flask import Flask
from flask_apispec import use_kwargs, marshal_with, FlaskApiSpec
from flask_bcrypt import Bcrypt

from marshmallow import fields, Schema

from modules.user.models import User

app = Flask(__name__)
docs = FlaskApiSpec(app)
bcrypt = Bcrypt(app)

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'created_at', 'updated_at', 'deleted_at')
    
@app.route('/pets')
@marshal_with(UserSchema(many=True))
def get_pets(**kwargs):
    return User.query.filter_by(**kwargs)

docs.register(get_pets)

if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0') 