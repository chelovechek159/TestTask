from clients.api_client import ApiClient
from conftest import create_vm_request_data, update_vm
from models.vm.get_vm_response import GetVmResponse


def test_create_vm(api_client: ApiClient):
    created_vm = create_vm_request_data()
    name = created_vm.vm_name
    password = created_vm.vm_password
    owner_id = created_vm.owner_id

    created_vm_response = api_client.create_vm(created_vm, name=name)
    vm_id = int(created_vm_response.text)
    get_vm_response = api_client.get_vm(vm_id)
    get_vm_data = GetVmResponse.from_json(get_vm_response.content)

    assert created_vm_response.status_code == 200, "VM was not created"
    assert get_vm_response.status_code == 200, "Status code is not 200"

    assert vm_id > 0, "Vm Id is incorrect"
    assert name == get_vm_data.vm_name, "Name is incorrect"
    assert password == get_vm_data.vm_password, "Password is incorrect"
    assert owner_id > 0 and owner_id == get_vm_data.owner_id, "Owner ID is incorrect"


def test_update_vm_name(api_client: ApiClient, create_vm):
    vm_id, vm_data = create_vm
    new_name = update_vm().vm_name
    vm_update_response = api_client.update_vm_name(vm_id, name=new_name)
    assert vm_update_response.status_code == 200, "VM is not updated"

    updated_vm_response = api_client.get_vm(vm_id)
    updated_vm = GetVmResponse.from_json(updated_vm_response.content)

    assert new_name == updated_vm.vm_name, "Name is invalid"
    assert vm_data.vm_password == updated_vm.vm_password, "Password is ivalid"
    assert vm_data.owner_id == updated_vm.owner_id, "OwnerId is invalid"
    assert vm_update_response.text == 'true', "Response body is not true"


def test_update_vm_owner_id(api_client: ApiClient, create_vm):
    vm_id, vm_data = create_vm
    new_owner = update_vm().owner_id
    vm_update_response = api_client.update_vm_owner(vm_id, owner_id=new_owner)
    assert vm_update_response.status_code == 200, "VM is not updated"

    updated_vm_response = api_client.get_vm(vm_id)
    updated_vm = GetVmResponse.from_json(updated_vm_response.content)

    assert vm_data.vm_name == updated_vm.vm_name, "Name is invalid"
    assert vm_data.vm_password == updated_vm.vm_password, "Password is ivalid"
    assert new_owner == updated_vm.owner_id, "OwnerId is invalid"
    assert vm_update_response.text == 'true'


def test_update_vm_password(api_client: ApiClient, create_vm):
    vm_id, vm_data = create_vm
    new_password = update_vm().vm_password
    vm_update_response = api_client.update_vm_password(vm_id, password=new_password)
    assert vm_update_response.status_code == 200, "VM is not updated"

    updated_vm_response = api_client.get_vm(vm_id)
    updated_vm = GetVmResponse.from_json(updated_vm_response.content)

    assert vm_data.vm_name == updated_vm.vm_name, "Name is invalid"
    assert new_password == updated_vm.vm_password, "Password is ivalid"
    assert vm_data.owner_id == updated_vm.owner_id, "OwnerId is invalid"


def test_delete_vm(api_client: ApiClient, create_vm):
    vm_id, vm_data = create_vm
    vm_delete_response = api_client.delete_vm(vm_id)
    get_vm_response = api_client.get_vm(vm_id)
    assert vm_delete_response.status_code == 200, "Status code is invalid"
    assert get_vm_response.status_code != 200, "User is not deleted"
