from utils.marshmallow import BaseSchema
from marshmallow import fields
from marshmallow_enum import EnumField
from .models import User, UserPermission, PermissionEnum

class UserSchema(BaseSchema):
    dump_only = ['created_at', 'updated_at', 'deleted_at', 'id']
    load_only = ['password']
    permissions = fields.Nested('UserPermissionSchema', exclude=['permissions'], many=True)

    class Meta:
        model = User

class UserPermissionSchema(BaseSchema):
    permission = fields.Str(dump_only=True)

    class Meta:
        model = UserPermission
