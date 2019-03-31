from flask import request, make_response
from flask_apispec import MethodResource

from modules.user.models import User
from modules.user.schemas import UserSchema
from utils.openapi import api
from utils import http_status

class UserResource(MethodResource):
    base_url = '/user'
    default_tag = 'User'

    @staticmethod
    @api(
        path='/',
        methods=['POST'],
        use_kwargs=UserSchema(),
        marshal_with=UserSchema(),
        description='This endpoint creates a User inside system'
    )
    def create_users(**kwargs):
        data = request.get_json()
        user_obj = UserSchema(strict=True).load(data)
        user_obj.data.save(flush=True, commit=True)

        return UserSchema(many=False).dump(user_obj.data).data
        

    @staticmethod
    @api(
        path='/',
        marshal_with=UserSchema(many=True),
    )
    def get_users():
        return UserSchema(many=True).dump(User.get_all()).data

    @staticmethod
    @api(
        path='/<int:id>',
        marshal_with=UserSchema(many=False),
    )
    def get_user(id):
        return UserSchema(many=False).dump(User.get(id)).data

    @staticmethod
    @api(
        path='/<int:id>',
        methods=['DELETE'],
        marshal_with={"204": {"description": "Bank information deleted"}},
    )
    def delete_user(id):
        user = User.get(id)
        user.delete()
        return make_response('', http_status.HTTP_204_NO_CONTENT)

    @staticmethod
    @api(
        path='/<int:id>',
        methods=['PUT'],
        use_kwargs=UserSchema(dump_only=["password"]),
        marshal_with=UserSchema(many=False),
    )
    #@acl.auth(permission=['COMMON'], is_same_author=True)
    def update_user(id):
        user_obj = UserSchema(dump_only=["password"], strict=True).load(
            request.get_json(), instance=User.get(id), partial=True
        )

        user_obj.data.save(commit=True)

        return UserSchema(many=False).dump(user_obj).data
