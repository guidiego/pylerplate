from marshmallow import fields, validates_schema, ValidationError, Schema

from .models import User, UserPermission
from utils.marshmallow import BaseSchema, BasePageReturnSchema
from utils.errors import AuthenticationError


class UserBaseSchema(BaseSchema):
    permissions = fields.Nested('UserPermissionSchema', exclude=[], many=True)
    dump_only = ['created_at', 'updated_at', 'deleted_at', 'id', 'permissions']

    class Meta:
        model = User


class UserPermissionSchema(BaseSchema):
    permission = fields.Str(dump_only=True)

    class Meta:
        model = UserPermission


class UserSchema(UserBaseSchema):
    exclude = ['password']


class UserInputSchema(Schema):
    name = fields.String()
    email = fields.String(allow_none=True)


class UserReturnSchema(BasePageReturnSchema):
    items = fields.Nested('UserSchema', exclude=[], many=True)


class PasswordUpdateSchema(Schema):
    password = fields.String()
    password_confirmation = fields.String()

    @validates_schema
    def validate_password_confirmation(self, schema):
        password = schema.get('password')
        password_confirmation = schema.get('password_confirmation')

        if not password == password_confirmation:
            # password_message = 'Password need to check with confirmation'
            # print('TEST')
            # raise ValidationError({
            #     'password_confirmation': password_message
            # })
            raise ValidationError({
                'password_confirmation': 'Password need to check with confirmation'
            })


class UserCreateSchema(PasswordUpdateSchema, UserBaseSchema):
    pass