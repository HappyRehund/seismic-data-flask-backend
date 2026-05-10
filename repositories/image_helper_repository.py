import os
import struct
from typing import Optional, List, Dict

from models.image_helper_model import ImageDimensions
from models.seismic_section_model import SectionType

SEISMIC_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'inline_crossline')


class ImageHelperRepository:
    def __init__(self):
        self._datasets: Dict[str, str] = {}
        self._section_types_cache: Dict[str, List[str]] = {}
        self._discover_datasets()

    def _discover_datasets(self):
        if not os.path.isdir(SEISMIC_DATA_DIR):
            raise FileNotFoundError(f"Seismic data directory not found: {SEISMIC_DATA_DIR}")

        for entry in sorted(os.listdir(SEISMIC_DATA_DIR)):
            full_path = os.path.join(SEISMIC_DATA_DIR, entry)
            if os.path.isdir(full_path):
                self._datasets[entry] = full_path
                self._section_types_cache[entry] = sorted([
                    d for d in os.listdir(full_path)
                    if os.path.isdir(os.path.join(full_path, d))
                ])

        if not self._datasets:
            raise FileNotFoundError(f"No dataset directories found in {SEISMIC_DATA_DIR}")

    def list_datasets(self) -> List[str]:
        return sorted(self._datasets.keys())

    def list_section_types(self, dataset: str) -> List[str]:
        if dataset not in self._datasets:
            available = sorted(self._datasets.keys())
            raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")
        return self._section_types_cache[dataset]

    def _get_base_path(self, dataset: str) -> str:
        if dataset not in self._datasets:
            available = sorted(self._datasets.keys())
            raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")
        return self._datasets[dataset]

    def _normalize_section_type(self, section_type: str) -> SectionType:
        for candidate in SectionType:
            if candidate.value == section_type:
                return candidate
        raise ValueError(
            "Unsupported section type. Use inline, crossline, inlineMJB, or crosslineMJB."
        )

    def _build_candidate_paths(self, section_type: SectionType, dataset: str, number: int) -> list[str]:
        base = self._get_base_path(dataset)

        if section_type == SectionType.INLINE:
            return [
                os.path.join(base, 'inline', f'inline_{number}.png'),
            ]

        if section_type == SectionType.CROSSLINE:
            return [
                os.path.join(base, 'crossline', f'crossline_{number}.png'),
            ]

        if section_type == SectionType.INLINEMJB:
            return [
                os.path.join(base, 'inlineMJB', f'inline_{number}.png'),
                os.path.join(base, 'inlineMJB', f'inlineMJB_{number}.png'),
            ]

        if section_type == SectionType.CROSSLINEMJB:
            return [
                os.path.join(base, 'crosslineMJB', 'crosslineMJB', f'crossline_{number}.png'),
                os.path.join(base, 'crosslineMJB', f'crossline_{number}.png'),
                os.path.join(base, 'crosslineMJB', f'crosslineMJB_{number}.png'),
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
        self, section_type: str, number: int, dataset: str = 'default'
    ) -> Optional[ImageDimensions]:
        if number < 1:
            raise ValueError("Section number must be positive")

        normalized_section_type = self._normalize_section_type(section_type)
        path = next(
            (
                candidate
                for candidate in self._build_candidate_paths(normalized_section_type, dataset, number)
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
