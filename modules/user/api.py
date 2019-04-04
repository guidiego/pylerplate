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
        use_kwargs=UserSchema(dump_only=['permissions']),
        marshal_with=UserSchema(),
        description='Create an User'
    )
    def create_users(**kwargs):
        data = request.get_json()
        user_obj = UserSchema(dump_only=['permissions'], strict=True).load(data)
        user_obj.data.save(flush=True, commit=True)

        permission = UserPermission.set_common(user_obj.data.id)
        permission.save(flush=True, commit=True)

        return UserSchema(many=False).dump(user_obj.data).data
        

    @staticmethod
    @acl(permission_to_ignore_rules=['COMMON'])
    @api(
        path='/',
        marshal_with=UserSchema(many=True),
        description='Get all Users'
    )
    def get_users():
        return UserSchema(many=True).dump(User.get_all()).data

    #TODO: Fix id error
    @staticmethod
    @acl(permission_to_ignore_rules=['COMMON'])
    @api(
        path='/<int:user_id>',
        marshal_with=UserSchema(many=False),
        description='Get an User'
    )
    def get_user(user_id):
        return UserSchema(many=False).dump(User.get(user_id)).data

    @staticmethod
    @acl(
        request_by_same_id=True,
        permission_to_ignore_rules=['ADMIN']
    )
    @api(
        path='/<int:id>',
        methods=['DELETE'],
        marshal_with={"204": {"description": "Bank information deleted"}},
        description='Delete an User'
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
        description='Update an User'
    )
    def update_user(**kwargs):
        user_id = request.view_args.get('user_id')
        user_obj = UserSchema(strict=True).load(
            kwargs, instance=User.get(user_id), partial=True
        )

        user_obj.data.save(flush=True, commit=True, pre_save=False)

        return UserSchema(many=False).dump(user_obj.data).data
