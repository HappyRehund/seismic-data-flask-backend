from typing import Any, Protocol, Mapping, List


class DtoResponse(Protocol):
    def to_dict(self) -> Mapping[str, Any]: ...


class ListResponse:
    """Generic wrapper for list responses that implements DtoResponse protocol"""
    def __init__(self, key: str, items: List[Any]):
        self._key = key
        self._items = items

    def to_dict(self) -> dict:
        return {
            self._key: [item.to_dict() for item in self._items],
            "count": len(self._items)
        }
