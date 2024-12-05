from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass(kw_only=True)
class GetVmResponse(DataClassJsonMixin):
    owner_id: int
    vm_name: str
    vm_password: str
