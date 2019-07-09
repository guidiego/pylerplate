from flask import request, make_response
from flask_apispec import MethodResource

from .models import User, UserPermission
from .schemas import (
    UserSchema, UserBaseSchema, UserCreateSchema,
    UserReturnSchema, UserInputSchema, PasswordUpdateSchema
)

from utils.openapi import api
from utils.page_method import page_method
from utils.acl import acl
from utils import http_status

class UserResource(MethodResource):
    base_url = '/user'
    default_tag = 'User'

    @staticmethod
    @api(
        path='/',
        methods=['POST'],
        use_kwargs=UserCreateSchema(strict=True),
        marshal_with=UserSchema(),
        summary='Criar Usuário',
        description='Permite criar um usuário no sistema',
    )
    def create_user(**kwargs):
        body = request.get_json()

        user_obj = UserCreateSchema(strict=True).load(body)
        user_obj.data.save(commit=True)

        permission = UserPermission.set_common(user_obj.data.id)
        permission.save(commit=True)

        return user_obj.data

    @staticmethod
    @api(
        path='/',
        marshal_with=UserReturnSchema(),
        summary='Listar Usuários',
        description='Permite listar todos os usuários',
    )
    @acl(only_for=['ADMIN'])
    def get_users_page():
        return page_method(User)

    @staticmethod
    @api(
        path='/<string:user_id>',
        marshal_with=UserSchema(),
        summary='Detalhes Usuário',
        description='Permite recuperar os detalhes de um usuário',
    )
    @acl()
    def get_user(user_id):
        return User.get(user_id)

    @staticmethod
    @api(
        path='/<string:user_id>',
        methods=['DELETE'],
        marshal_with={"204": {"description": "Bank information deleted"}},
        summary='Deletar Usuário',
        description='Permite remover um usuário do sistema',
    )
    @acl(
        request_by_same_id=True,
        permission_to_ignore_rules=['ADMIN']
    )
    def delete_user(user_id):
        user = User.get(user_id)
        user.delete(commit=True, flush=True)
        return make_response('', http_status.HTTP_204_NO_CONTENT)

    @staticmethod
    @api(
        path='/<string:user_id>',
        methods=['PUT'],
        use_kwargs=UserInputSchema(strict=True),
        marshal_with=UserSchema(),
        summary='Atuaizar Usuário',
        description='Permite editar dados do usuário no sistema',
    )
    @acl(
        request_by_same_id=True,
        permission_to_ignore_rules=['ADMIN']
    )
    def update_user(**kwargs):
        user_id = request.view_args.get('user_id')

        user_obj = UserSchema(strict=True).load(
            kwargs, instance=User.get(user_id), partial=True
        )

        user_obj.data.save(flush=True, commit=True, pre_save=False)

        return user_obj.data

    @staticmethod
    @api(
        path='/change-password',
        methods=['PUT'],
        use_kwargs=PasswordUpdateSchema(),
        marshal_with={"204": {"description": "Database information deleted"}},
        summary='Trocar Senha',
        description='Permite trocar a senha do usuário no sistema',
    )
    @acl()
    def change_password(**kwargs):
        print(request.context.user)
        # user_obj = PasswordUpdateSchema(strict=True).load(
        #     kwargs, instance=request.context.user, partial=True
        # )
        user_obj = PasswordUpdateSchema(strict=True).load(
            kwargs, instance=User.get('53a42735-0410-4612-8283-529c560d1677'), partial=True
        )

        user_obj.data.save(flush=True, commit=True)

        return make_response('', http_status.HTTP_204_NO_CONTENT)
