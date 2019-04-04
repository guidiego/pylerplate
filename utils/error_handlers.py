import logging
from flask import jsonify
from marshmallow.exceptions import ValidationError


class BaseError(Exception):
    status_code = 447
    payload = {}

    def __init__(self, error_code, status_code=None, payload=None):
        Exception.__init__(self)
        self.error_code = error_code

        if status_code is not None:
            self.status_code = status_code

        if payload is not None:
            self.payload = payload


    def handle_error(self):
        logging.exception('Application Error', extra={'stack': True})
        response = jsonify({'error_code': self.error_code, 'payload': self.payload})
        response.status_code = self.status_code
        return response

def handle_marshmallow_error(marshmallow_error):

    response = jsonify({'error_code': 4, 'payload': marshmallow_error.messages})
    response.status_code = BaseError.status_code
    return response

def internal_server_handler(e):
    logging.exception('Internal Server Error', extra={'stack': True})
    response = jsonify({'Error': 0})
    response.status_code = 500
    return response

