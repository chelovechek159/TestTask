import pytest
from clients.api_client import ApiClient
from infrastructure.config import Config
from models.user.create_user_request import CreateUserRequest
from faker import Faker
from models.user.get_user_response import GetUserResponse
from models.user.update_user_request import UpdateUserRequest
from models.vm.create_vm_request import CreateVmRequest
from models.vm.get_vm_response import GetVmResponse
from models.vm.update_vm_response import UpdateVmResponse
from utils import get_random_hex_string

fake = Faker()


@pytest.fixture(scope='session')
def api_client() -> ApiClient:
    login = Config().get_login()
    password = Config().get_password()
    api_client = ApiClient()
    api_client.set_access_token(login=login, password=password)
    return api_client


def create_user_request_data() -> CreateUserRequest:
    req_data = CreateUserRequest(
        password=get_random_hex_string(),
        name=fake.name(),
    )
    return req_data


@pytest.fixture(scope="function")
def create_user(api_client: ApiClient) -> GetUserResponse:
    created_user = create_user_request_data()
    name = created_user.name
    password = created_user.password
    create_user_response = api_client.create_user(name, password)

    get_user_response = api_client.get_user(created_user.name)
    get_user_data = GetUserResponse.from_json(get_user_response.content)

    assert create_user_response.status_code == 200, "User was not created"
    assert get_user_response.status_code == 200, "Status code is not 200"

    return get_user_data


def update_user_data() -> UpdateUserRequest:
    req_body = UpdateUserRequest(
        password=get_random_hex_string()
    )
    return req_body


def create_vm_request_data() -> CreateVmRequest:
    req_data = CreateVmRequest(
        owner_id=fake.random_int(10, 99999, 1),
        vm_password=get_random_hex_string(),
        vm_name=fake.name(),
    )
    return req_data


@pytest.fixture(scope="function")
def create_vm(api_client: ApiClient) -> tuple[int, GetVmResponse]:
    created_vm = create_vm_request_data()
    name = created_vm.vm_name

    created_vm_response = api_client.create_vm(created_vm, name=name)
    vm_id = int(created_vm_response.text)
    get_vm_response = api_client.get_vm(vm_id)
    get_vm_data = GetVmResponse.from_json(get_vm_response.content)

    assert created_vm_response.status_code == 200, "VM was not created"
    assert get_vm_response.status_code == 200, "Status code is not 200"

    assert vm_id > 0, "Vm Id is incorrect"
    return vm_id, get_vm_data


def update_vm() -> UpdateVmResponse:
    req_body = UpdateVmResponse(
        vm_name=fake.user_name(),
        vm_password=get_random_hex_string(),
        owner_id=fake.random_int(11, 99999, 1)
    )
    return req_body
