import uuid

from flask import request
from flask_apispec import MethodResource

from modules.auth.schemas import AuthSchema, AuthReturnSchema
from modules.user.models import User
from utils.openapi import api
from utils.acl import acl

from app import auth_token_db

hour_in_secs = 1 * 60 * 60


def auth_logic(user):
    save_item = user.id
    token = str(uuid.uuid4())

    auth_token_db.set(token, save_item, ex=hour_in_secs)

    return {
        'token': token,
        'user': user
    }


class AuthResource(MethodResource):
    base_url = '/auth'
    default_tag = 'Auth'

    @staticmethod
    @api(
        path='/',
        methods=['POST'],
        use_kwargs=AuthSchema(strict=True),
        marshal_with=AuthReturnSchema(),
        summary='Criar Acesso',
        description='Esse endpoint espera as credenciais para criar o acesso, por definição é retornado o usuário de trabalho',
    )
    def create_auths(**kwargs):
        return auth_logic(
            User.verify_credentials(**kwargs)
        )

    @staticmethod
    @api(
        path='/',
        marshal_with=AuthReturnSchema(),
        summary='Dados da Sessão',
        description='Esse endpoint retorna dados atualizados da sessão',
    )
    @acl()
    def get_auths():
        return {
            'token': request.context.token,
            'user': request.context.user,
        }
