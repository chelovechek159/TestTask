from clients.api_client import ApiClient
from models.user.get_user_response import GetUserResponse
from conftest import create_user_request_data, update_user_data


def test_user_create(api_client: ApiClient):
    created_user = create_user_request_data()
    name = created_user.name
    password = created_user.password
    create_user_response = api_client.create_user(name, password)

    get_user_response = api_client.get_user(created_user.name)
    get_user_data = GetUserResponse.from_json(get_user_response.content)

    assert create_user_response.status_code == 200, "User was not created"
    assert get_user_response.status_code == 200, "Status code is not 200"

    assert name == get_user_data.name, "Name is incorrect"
    assert password == get_user_data.password, "Password is incorrect"
    assert get_user_data.id > 0, "User ID is incorrect"


def test_update_password(api_client: ApiClient, create_user):
    name = create_user.name
    new_password = update_user_data().password
    user_update_response = api_client.update_user(name, new_password)
    assert user_update_response.status_code == 200, "User is not updated"
    updated_user_response = api_client.get_user(name)
    updated_user = GetUserResponse.from_json(updated_user_response.content)

    assert name == updated_user.name, "Name is invalid"
    assert create_user.id == updated_user.id, "Id is invalid"
    assert create_user.password != new_password == updated_user.password, "Password is invalid"


def test_delete_user(api_client: ApiClient, create_user):
    name = create_user.name
    delete_user_response = api_client.delete_user(name=name)
    get_user_response = api_client.get_user(name)

    assert delete_user_response.text == 'true', "Response body is not true"
    assert delete_user_response.status_code == 200, "Status code is invalid"
    assert get_user_response.status_code != 200, "User is not deleted"


