from typing import Any, Protocol, Mapping


class DtoResponse(Protocol):
    def to_dict(self) -> Mapping[str, Any]: ...
