from modules.user.api import UserResource


def test_get_user_should_back_empty_list():
    resource = UserResource()
    assert resource.get() == []