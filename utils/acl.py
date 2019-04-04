import json

from flask import request
from functools import wraps
from app import app

from .errors import AuthenticationError

def acl(request_by_same_id=False, only_for=[], permission_to_ignore_rules=[], additional_headers=[]):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            required_keys = ['permissions', 'id']
            header = request.headers.get(app.config['REQUEST_AUTHOR_ID']) or '{}'
            req_user = json.loads(header)

            if not all(key in req_user for key in required_keys):
                missing_keys = [x for x in set(required_keys) - req_user.keys()]
                raise AuthenticationError(error_code=0, payload={ 'missing_keys': missing_keys })

            if not any(permission in permission_to_ignore_rules for permission in req_user['permissions']):
                if request_by_same_id and request.view_args.get('user_id') != req_user['id']:
                    raise AuthenticationError(error_code=1)

                if only_for and not any(permission in only_for for permission in req_user['permissions']):
                    raise AuthenticationError(error_code=2)


            return func(*args, **kwargs)
            
        if hasattr(decorated_function, '__docs__'):
            decorated_function.__docs__ = {}

        
        additional_headers.append(app.config['REQUEST_AUTHOR_ID'])

        for i in additional_headers:
            decorated_function.__docs__['params'] = { i: {"in": "header", "type": "object", "properties": {"id": {"type": "integer"}}, "required": True} }

        return decorated_function
    return decorator

# @acl(
#     request_by_same_id=True,
#     only_for=['COMMON', 'EDITORS'],
#     permissions_to_ignore_rules=['ADMIN'],
#     # additional_headers=[acl.header('other', 'string')]
# )