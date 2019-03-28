from marshmallow import Schema

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'created_at', 'updated_at', 'deleted_at')