from utils.openapi import MethodResource, api
from modules.user.models import User
from modules.user.schemas import UserSchema

class UserResource(MethodResource):
    base_url = '/users'

    @api(
        path='/',
        methods=['POST'],
        use_kwargs=UserSchema(),
        marshal_with=UserSchema(),
    )
    def create_users(self):
        return {}

    @api(
        path='/',
        marshal_with=UserSchema(many=True),
    )
    def get_users(self):
        return []
