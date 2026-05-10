import os
from typing import Optional, List, Dict
from models.seismic_section_model import SeismicSection, SectionType

SEISMIC_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'inline_crossline')


class SeismicSectionRepository:
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

    def find_by_number(
        self, section_type: SectionType, number: int, dataset: str = 'default'
    ) -> Optional[SeismicSection]:
        path = next(
            (candidate for candidate in self._build_candidate_paths(section_type, dataset, number)
             if os.path.exists(candidate)),
            None,
        )
        if path is None:
            return None

        with open(path, 'rb') as f:
            image_data = f.read()

        return SeismicSection(
            section_type=section_type,
            section_number=number,
            image_data=image_data,
        )
