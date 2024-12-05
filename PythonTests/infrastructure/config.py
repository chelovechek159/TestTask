import json
import os
from functools import lru_cache
from from_root import from_root

CONFIG_FILE_NAME = "config.json"


@lru_cache
class Config:
    __config: dict

    def __init__(self):
        try:
            with open(os.path.join(from_root(), CONFIG_FILE_NAME)) as f:
                self.__config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"No {CONFIG_FILE_NAME} file found")

    def get(self, key: str):
        return self.__config.get(key)

    def get_url(self):
        return self.__config.get("url")

    def get_login(self):
        return self.__config.get("login")

    def get_password(self):
        return self.__config.get("password")
