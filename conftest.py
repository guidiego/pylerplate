
import pytest

from app import create_app, db

from modules.user.models import User
from modules.auth.api import auth_logic


@pytest.fixture(scope='session')
def test_client(request):
    flask_app = create_app()

    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    @request.addfinalizer
    def teardown():
        ctx.pop()

    return testing_client


@pytest.fixture(scope='session')
def _db(test_client, request):
    db.create_all()

    @request.addfinalizer
    def teardown():
        db.session.close()
        db.drop_all()

    return db


@pytest.fixture(scope='session')
def new_user(_db):
    user = User(email='test@test.com', name='Test', password='123456')
    user.save(commit=True)

    return user


@pytest.fixture(scope='session')
def token_obj(new_user):

    token = auth_logic(new_user)

    return token
