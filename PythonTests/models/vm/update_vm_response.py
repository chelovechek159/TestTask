from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config


def exclude_if_none(x) -> bool:
    return x is None


@dataclass(kw_only=True)
class UpdateVmResponse(DataClassJsonMixin):
    owner_id: int = field(default=None, metadata=config(exclude=exclude_if_none))
    vm_name: str = field(default=None, metadata=config(exclude=exclude_if_none))
    vm_password: str = field(default=None, metadata=config(exclude=exclude_if_none))
