from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass(kw_only=True)
class GetUserResponse(DataClassJsonMixin):
    id: int
    name: str
    password: str
