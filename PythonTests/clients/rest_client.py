import abc
import os
from http import HTTPMethod
import requests
from requests import Response


class RestClient(abc.ABC):
    __url: str  # Определены как приватные атрибуты (с двойным подчеркиванием),
    __headers: dict  # чтобы их нельзя было случайно изменить вне класса.

    # инициализирует объект RestClient
    def __init__(self, url: str):
        self.__url = url
        self.__headers = {}

    # Добавляет заголовки в словарь, обновляя перед каждым запросом
    def _add_headers(self, headers: dict) -> None:
        self.__headers.update(headers)

    def _get_headers(self) -> dict:
        return self.__headers.copy()

    # Отправляет запрос с параметрами
    def _send_request(
        self,
        *,  # все параметры после * должны быть явно указаны
        method: HTTPMethod,
        paths: list[str] = None,  # список частей пути для URL
        headers: dict = None,
        params: dict = None,
        json_body: dict = None,
        data: str = None
    ) -> Response:
        url = self._get_full_url(paths)
        headers = self._join_headers(headers)

        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            headers=headers,
            data=data
        )
        return response

    # Метод для формирования полного URL из базового URL и списка путей
    def _get_full_url(self, paths: list[str] | None) -> str:
        if paths is None:
            paths = []  # Если путь пустой, устанавливается пустой список
        paths_list = filter(lambda x: x, paths)  # Фильтрация пустых элементов в путях
        return os.path.join(self.__url, *paths_list)  # Объединение базового URL и отфильтрованных путей

    def _join_headers(self, headers: dict | None) -> dict:
        if headers is None:
            headers = {}  # Если заголовки не заданы, создается пустой словарь
        headers.update(self.__headers)  # Обновление словаря переданными заголовками
        return headers
