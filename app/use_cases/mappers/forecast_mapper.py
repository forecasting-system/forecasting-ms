import json

from dataclasses import asdict, is_dataclass
from typing import Any


def dataclass_to_nats_payload(obj: Any) -> bytes:
    if not is_dataclass(obj) or isinstance(obj, type):
        raise TypeError("Expected a dataclass instance")

    dataclass_dict = asdict(obj)
    return json.dumps(dataclass_dict, default=str).encode("utf-8")
