from flask import Flask
from flask_apispec import use_kwargs, marshal_with

from marshmallow import fields, Schema

from modules.user.models import User

app = Flask(__name__)

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'created_at', 'updated_at', 'deleted_at')

@app.route('/pets')
@use_kwargs({'category': fields.Str(), 'size': fields.Str()})
@marshal_with(UserSchema(many=True))
def get_pets(**kwargs):
    return User.query.filter_by(**kwargs)

if __name__ == "__main__":
    app.run(debug=True)