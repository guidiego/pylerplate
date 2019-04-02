from flask import request
from functools import wraps
from app import app
# from config import Config


# TODO: Implement it
def acl(request_by_same_id=False, only_for=[], permission_to_ignore_rules=[], additional_headers=[]):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
        
            req_user = {'user_id': request.headers.get(app.config['REQUEST_AUTHOR_ID'])}
            print(req_user)
        # request_by_same_id == True -> request.view_args(id) == req_user.id
            # só nao vai rolar se 1 das permisoes do req_user tive dentro `allow_for`
        # throw -> Como funciona o flask handle no nosso caso com o marshamallow
            return func(*args, **kwargs)

        if hasattr(decorated_function, '__docs__'):
            decorated_function.__docs__ = {}

        
        additional_headers.append(app.config['REQUEST_AUTHOR_ID'])

        for i in additional_headers:
            decorated_function.__docs__['params'] = { i: {"in": "header", "type": "string", "required": True} }

        return decorated_function
    return decorator

# @acl(
#     request_by_same_id=True,
#     only_for=['COMMON', 'EDITORS'],
#     permissions_to_ignore_rules=['ADMIN'],
#     # additional_headers=[acl.header('other', 'string')]
# )