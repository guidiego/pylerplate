from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from utils.error_handlers import (
    handle_marshmallow_error, internal_server_handler,
    db_integrity_error, BaseError
)


class Diag:
    constraint_name = 'Test'


class Orig:
    diag = Diag


def test_base_error():
    base_error = BaseError(Exception)
    base_error_custom = BaseError(error_code=0,
                                  status_code=445,
                                  payload={'error': 'test'})

    response = base_error_custom.handle_error()

    assert base_error.status_code == 447
    assert base_error.payload == {}
    assert response.status_code == 445
    assert response.data == b'{"error_code":0,"payload":{"error":"test"}}\n'


def test_handle_marshmallow_error():
    exception = ValidationError('Test Error')
    response = handle_marshmallow_error(exception)

    assert response.status_code == 447
    assert response.data == b'{"error_code":4,"payload":["Test Error"]}\n'


def test_internal_server_handler():
    response = internal_server_handler(Exception)

    assert response.status_code == 500
    assert response.data == b'{"Error":0}\n'


def test_db_integrity_error():
    exception = IntegrityError('Test Error', {}, Orig)
    response = db_integrity_error(exception)

    assert response.status_code == 447
    assert response.data == b'{"error_code":5,"payload":{"Test":"Esse dado j\\u00e1 consta no banco!"}}\n'
