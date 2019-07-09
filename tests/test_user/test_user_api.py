import json

from app import bcrypt


def test_get_users(test_client):
    response = test_client.get("/user")

    response_json = json.loads(response.data)

    assert response.status_code == 200

    assert 'page' in response_json and \
           isinstance(response_json['page'], (type(None), str)) is True
    assert 'total' in response_json and \
           isinstance(response_json['total'], int) is True
    assert 'items' in response_json and \
           isinstance(response_json['items'], list) is True


def test_get_user(test_client, new_user):
    response = test_client.get("/user/{}".format(new_user.id))

    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert response_json['id'] == new_user.id


def test_update_user(test_client, new_user, token_obj):
    token_header = {'x-authorization': token_obj['token']}

    update_data = {
        'name': 'Test Update'
    }

    response = test_client.put("/user/{}".format(token_obj['user'].id),
                               data=update_data,
                               headers=token_header)

    response_json = json.loads(response.data)

    assert response_json['name'] == update_data['name']
    assert response.status_code == 200


def test_user_change_password(test_client, new_user, token_obj):
    token_header = {'x-authorization': token_obj['token']}

    update_password_data = {
        'password': '654321',
        'password_confirmation': '654321'
    }

    response = test_client.put("/user/change-password",
                               data=update_password_data,
                               headers=token_header)

    assert response.status_code == 204
    assert bcrypt.check_password_hash(
        new_user.password,
        update_password_data['password']
    ) is True


def test_delete_user(test_client, new_user, token_obj):
    token_header = {'x-authorization': token_obj['token']}

    response = test_client.delete("/user/{}".format(token_obj['user'].id),
                                  headers=token_header)

    assert response.status_code == 204
