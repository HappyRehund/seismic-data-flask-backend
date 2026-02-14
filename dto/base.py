from typing import Dict, Any, Protocol


class DtoResponse(Protocol):
    def to_dict(self) -> Dict[str, Any]: ...
