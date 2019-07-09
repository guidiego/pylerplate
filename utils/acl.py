import json

from flask import request
from functools import wraps

from app import auth_token_db
from config import Config
from modules.user.models import User

from .errors import AuthenticationError


class Ctx:
    user = None
    token = None

    def __init__(self, token, user):
        self.token = token
        self.user = user


def acl(request_by_same_id=False, only_for=[], permission_to_ignore_rules=[], additional_headers=[]):
    def decorator(func):
        header_name = Config.REQUEST_AUTHOR_ID

        payload_header = {'missing_header': header_name}
        payload_token = {'token': 'Invalid token'}
        payload_user = {'invalid_user': 'User not associated with token'}

        @wraps(func)
        def decorated_function(*args, **kwargs):
            header = request.headers.get(header_name)

            if not header:
                raise AuthenticationError(error_code=0, payload=payload_header)

            req_user_id = auth_token_db.get(header).decode()
            req_user = User.get(req_user_id)

            if not req_user_id or not req_user:
                raise AuthenticationError(error_code=0, payload=payload_token)

            request.context = Ctx(
                header,
                req_user,
            )

            if not any(permission.permission.name in permission_to_ignore_rules for permission in req_user.permissions):
                if request_by_same_id and request.view_args.get('user_id') != req_user.id:
                    raise AuthenticationError(error_code=1, payload=payload_user)

                if only_for and not any(permission.permission.name in only_for for permission in req_user.permissions):
                    raise AuthenticationError(error_code=2, status_code=403, payload={'reason': 'permission'})

            return func(*args, **kwargs)
            
        if not hasattr(decorated_function, '__docs__'):
            decorated_function.__docs__ = {}


        additional_headers.append(header_name)

        for i in additional_headers:
            decorated_function.__docs__['params'] = { i: {"in": "header", "type": "object", "properties": {"id": {"type": "integer"}}, "required": True} }

        if not hasattr(decorated_function, '__docs__'):
            decorated_function.__docs__ = {}

        decorated_function.__docs__['params'] = {
            header_name: {
                "in": "header",
                "type": "string",
                "required": True
            }
        }

        return decorated_function
    return decorator
