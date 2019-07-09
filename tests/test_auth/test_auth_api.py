import json


def test_post_token(test_client, new_user):
    auth_data = {
        'email': new_user.email,
        'password': '123456'
    }

    response = test_client.post("/auth", data=auth_data)

    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert 'token' in response_json
    assert response_json['user']['id'] == new_user.id


def test_get_token(test_client, new_user, token_obj):
    token_header = {'x-authorization': token_obj['token']}
    response = test_client.get("/auth", headers=token_header)

    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert 'token' in response_json
    assert response_json['user']['id'] == new_user.id
