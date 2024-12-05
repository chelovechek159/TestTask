from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass(kw_only=True)
class CreateUserRequest(DataClassJsonMixin):
    name: str
    password: str
