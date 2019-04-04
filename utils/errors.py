# from marshmallow.exceptions import ValidationError
from .error_handlers import BaseError

class AuthenticationError(BaseError):

    def __init__(self, error_code, payload = {}):
        BaseError.__init__(self, error_code=error_code, status_code=401, payload=payload)
