import base64
from http import HTTPMethod
from typing import Self
from requests import Response
from clients.rest_client import RestClient
from infrastructure.config import Config
from models.vm.create_vm_request import CreateVmRequest


class ApiClient(RestClient):
    def __init__(self):
        url = Config().get_url()
        super().__init__(url)  # Инициализируем родительский класс с этим URL
        self._add_headers({"Content-Type": "application/json"})

    def set_access_token(self, login, password) -> Self:
        credentials = f"{login}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self._add_headers({'Authorization': f'Basic {encoded_credentials}'})
        return self

    def create_user(self, name: str, password: str) -> Response:
        response = self._send_request(method=HTTPMethod.GET, paths=[f"user/create/{name}/{password}"])
        return response

    def get_user(self, name: str) -> Response:
        response = self._send_request(method=HTTPMethod.GET, paths=[f"user/getinfo/{name}"])
        return response

    def update_user(self, name: str, password: str) -> Response:
        response = self._send_request(method=HTTPMethod.GET, paths=[f"user/change-password/{name}/{password}"])
        return response

    def delete_user(self, name: str) -> Response:
        response = self._send_request(method=HTTPMethod.DELETE, paths=[f"user/delete/{name}"])
        return response

    def create_vm(self, request: CreateVmRequest, name: str) -> Response:
        response = self._send_request(method=HTTPMethod.POST, paths=[f"vm/create/{name}"], json_body=request.to_dict())
        return response

    def get_vm(self, id: int) -> Response:
        response = self._send_request(method=HTTPMethod.GET, paths=[f"vm/getinfo/{id}"])
        return response

    def update_vm_name(self, id: int, name: str) -> Response:
        response = self._send_request(method=HTTPMethod.GET, paths=[f"vm/update/name/{id}/{name}"])
        return response

    def update_vm_owner(self, id: int, owner_id: int) -> Response:
        response = self._send_request(method=HTTPMethod.GET, paths=[f"vm/update/owner/{id}/{owner_id}"])
        return response

    def update_vm_password(self, id: int, password: str) -> Response:
        response = self._send_request(method=HTTPMethod.GET, paths=[f"vm/update/password/{id}/{password}"])
        return response

    def delete_vm(self, id: int) -> Response:
        response = self._send_request(method=HTTPMethod.DELETE, paths=[f"vm/delete/{id}"])
        return response
