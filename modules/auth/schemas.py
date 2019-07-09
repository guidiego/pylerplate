from marshmallow import Schema, fields


class AuthSchema(Schema):
    email = fields.String()
    password = fields.String()


class AuthReturnSchema(Schema):
    token = fields.String()
    user = fields.Nested('UserSchema', exclude=[], many=False)
