import os
import struct
from typing import Optional

from models.image_helper_model import ImageDimensions
from models.seismic_section_model import SectionType


class ImageHelperRepository:
    def __init__(self, base_path: str = 'csv_data/inline_crossline'):
        self.base_path = base_path

    def _normalize_section_type(self, section_type: str) -> SectionType:
        for candidate in SectionType:
            if candidate.value == section_type:
                return candidate
        raise ValueError(
            "Unsupported section type. Use inline, crossline, inlineMJB, or crosslineMJB."
        )

    def _build_candidate_paths(self, section_type: SectionType, number: int) -> list[str]:
        if section_type == SectionType.INLINE:
            return [
                os.path.join(self.base_path, 'inline', f'inline_{number}.png'),
            ]

        if section_type == SectionType.CROSSLINE:
            return [
                os.path.join(self.base_path, 'crossline', f'crossline_{number}.png'),
            ]

        if section_type == SectionType.INLINEMJB:
            return [
                os.path.join(self.base_path, 'inlineMJB', f'inline_{number}.png'),
                os.path.join(self.base_path, 'inlineMJB', f'inlineMJB_{number}.png'),
            ]

        if section_type == SectionType.CROSSLINEMJB:
            return [
                os.path.join(
                    self.base_path,
                    'crosslineMJB',
                    'crosslineMJB',
                    f'crossline_{number}.png',
                ),
                os.path.join(self.base_path, 'crosslineMJB', f'crossline_{number}.png'),
                os.path.join(
                    self.base_path,
                    'crosslineMJB',
                    f'crosslineMJB_{number}.png',
                ),
            ]

        return []

    def _read_png_dimensions(self, image_path: str) -> tuple[int, int]:
        with open(image_path, 'rb') as image_file:
            png_signature = image_file.read(8)
            if png_signature != b'\x89PNG\r\n\x1a\n':
                raise ValueError(f"File is not a valid PNG image: {image_path}")

            ihdr_length = struct.unpack('>I', image_file.read(4))[0]
            ihdr_type = image_file.read(4)
            if ihdr_type != b'IHDR' or ihdr_length < 8:
                raise ValueError(f"Invalid PNG header: {image_path}")

            width, height = struct.unpack('>II', image_file.read(8))
            return width, height

    def find_image_dimensions(
        self, section_type: str, number: int
    ) -> Optional[ImageDimensions]:
        if number < 1:
            raise ValueError("Section number must be positive")

        normalized_section_type = self._normalize_section_type(section_type)
        path = next(
            (
                candidate
                for candidate in self._build_candidate_paths(normalized_section_type, number)
                if os.path.exists(candidate)
            ),
            None,
        )

        if path is None:
            return None

        width, height = self._read_png_dimensions(path)
        return ImageDimensions(
            section_type=normalized_section_type.value,
            section_number=number,
            width=width,
            height=height,
            image_path=path,
        )