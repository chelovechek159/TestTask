from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass(kw_only=True)
class UpdateUserRequest(DataClassJsonMixin):
    password: str
