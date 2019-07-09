import pytest

from app import bcrypt

from modules.user.models import User
from utils.errors import AuthenticationError

user_info = {
    'email': 'test2@test.com',
    'name': 'Test2',
    'password': '123456'
}


def test_create_user():
    new_user = User(**user_info)
    new_user.save()

    assert new_user.email == user_info['email']
    assert new_user.name == user_info['name']
    assert bcrypt.check_password_hash(
        new_user.password,
        user_info['password']
        ) is True


def test_user_credentials():
    user = User.verify_credentials(user_info['email'], user_info['password'])
    assert user.email == user_info['email']


def test_user_failed_credentials():

    with pytest.raises(AuthenticationError):
        User.verify_credentials(
            'credentials_test@test.com',
            user_info['password']
        )
