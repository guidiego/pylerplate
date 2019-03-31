from flask import request


# TODO: Implement it
def acl(request_by_same_id=False, allow_for=[]):
    def decorator(func):
        return func

    return decorator