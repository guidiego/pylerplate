import json

from flask import request
from functools import wraps
from app import app

def acl(request_by_same_id=False, only_for=[], permission_to_ignore_rules=[], additional_headers=[]):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            header = request.headers.get(app.config['REQUEST_AUTHOR_ID'])

            if not header:
                raise Exception('Your {} header cannot be empty'.format(app.config['REQUEST_AUTHOR_ID']))
            
            req_user = json.loads(header)
            print(req_user['permissions'])

            # TODO: Improve Throw to be handler by Flask Error Handler (check marshmallow to put everything on a pattern)
            if not any(permission in permission_to_ignore_rules for permission in req_user['permissions']):
                if request_by_same_id and request.view_args.get('user_id') != req_user['id']:
                    raise Exception('Need Same Id!')

                if only_for and not any(permission in only_for for permission in req_user['permissions']):
                    raise Exception('You not have permission!')


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