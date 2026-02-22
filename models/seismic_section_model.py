from dataclasses import dataclass
from enum import Enum


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
