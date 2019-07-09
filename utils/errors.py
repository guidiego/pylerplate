from .error_handlers import BaseError


class AuthenticationError(BaseError):
    def __init__(self, error_code, status_code=401, payload={}):
        BaseError.__init__(self,
                           error_code=error_code,
                           status_code=status_code,
                           payload=payload)


class FieldError(BaseError):
    def __init__(self, error_code, payload={}):
        BaseError.__init__(self, error_code=error_code, payload=payload)
