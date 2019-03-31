from utils.marshmallow import BaseSchema
from .models import User

class UserSchema(BaseSchema):
    dump_only = ['created_at', 'updated_at', 'deleted_at', 'id', 'permissions']
    load_only = ['password']

    class Meta:
        model = User
