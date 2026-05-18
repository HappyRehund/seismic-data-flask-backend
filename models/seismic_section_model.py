from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class SectionType(Enum):
    INLINE = 'inline'
    CROSSLINE = 'crossline'


@dataclass
class SeismicSection:
    """Represents a seismic section image.

    In production with PostgreSQL, the `image_data` field maps to a
    bytea column storing the raw PNG bytes.
    """
    section_type: SectionType
    section_number: int
    image_data: bytes          # bytea in PostgreSQL

    def validate(self) -> bool:
        if self.section_number < 1:
            raise ValueError("Section number must be positive")
        if not self.image_data:
            raise ValueError("Image data must not be empty")
        return True


@dataclass
class SectionRange:
    """Represents min/max/count/range statistics for a section type."""
    min: int
    max: int
    count: int
    range: int = 0

    def __post_init__(self):
        self.range = self.max - self.min

    def to_dict(self) -> dict:
        return {
            "min": self.min,
            "max": self.max,
            "count": self.count,
            "range": self.range,
        }


@dataclass
class SeismicRangesResponse:
    """Response for seismic section ranges endpoint."""
    dataset: str
    ranges: Dict[str, Optional[SectionRange]]

    def to_dict(self) -> dict:
        result = {"dataset": self.dataset}
        ranges_dict = {}
        for key, value in self.ranges.items():
            ranges_dict[key] = value.to_dict() if value else None
        result["ranges"] = ranges_dict
        return result
