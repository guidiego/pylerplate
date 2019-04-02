from flask import request, make_response
from flask_apispec import MethodResource

from modules.user.models import User, UserPermission
from modules.user.schemas import UserSchema
from utils.openapi import api
from utils.acl import acl
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

        permission = UserPermission.set_common(user_obj.data.id)
        permission.save(flush=True, commit=True)

        return UserSchema(many=False).dump(user_obj.data).data
        

    @staticmethod
    @acl(permission_to_ignore_rules=['COMMON'])
    @api(
        path='/',
        marshal_with=UserSchema(many=True),
        description='This endpoint creates a User inside system'
    )
    def get_users():
        return UserSchema(many=True).dump(User.get_all()).data

    @staticmethod
    @acl(permission_to_ignore_rules=['COMMON'])
    @api(
        path='/<int:id>',
        marshal_with=UserSchema(many=False),
    )
    def get_user(id):
        return UserSchema(many=False).dump(User.get(id)).data

    @staticmethod
    @acl(
        request_by_same_id=True,
        permission_to_ignore_rules=['ADMIN']
    )
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
    @acl(
        request_by_same_id=True,
        permission_to_ignore_rules=['ADMIN']
    )
    @api(
        path='/<int:user_id>',
        methods=['PUT'],
        use_kwargs=UserSchema(exclude=['password']),
        marshal_with=UserSchema(many=False),
    )
    def update_user(**kwargs):
        user_id = request.view_args.get('user_id')
        user_obj = UserSchema(strict=True).load(
            kwargs, instance=User.get(user_id), partial=True
        )

        user_obj.data.save(flush=True, commit=True, pre_save=False)

        return UserSchema(many=False).dump(user_obj.data).data
