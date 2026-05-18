import os
from typing import List, Dict, ClassVar

SEISMIC_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'inline_crossline')


class BaseSeismicRepository:
    """Base repository with shared dataset-discovery logic.

    Class-level caches ensure the filesystem is scanned only once,
    regardless of how many repository instances are created.
    """
    _datasets: ClassVar[Dict[str, str]] = {}
    _section_types_cache: ClassVar[Dict[str, List[str]]] = {}
    _initialized: ClassVar[bool] = False

    def __init__(self):
        if not BaseSeismicRepository._initialized:
            self._discover_datasets()
            BaseSeismicRepository._initialized = True

    def _discover_datasets(self):
        if not os.path.isdir(SEISMIC_DATA_DIR):
            raise FileNotFoundError(f"Seismic data directory not found: {SEISMIC_DATA_DIR}")

        for entry in sorted(os.listdir(SEISMIC_DATA_DIR)):
            full_path = os.path.join(SEISMIC_DATA_DIR, entry)
            if os.path.isdir(full_path):
                BaseSeismicRepository._datasets[entry] = full_path
                BaseSeismicRepository._section_types_cache[entry] = sorted([
                    d for d in os.listdir(full_path)
                    if os.path.isdir(os.path.join(full_path, d))
                ])

        if not BaseSeismicRepository._datasets:
            raise FileNotFoundError(f"No dataset directories found in {SEISMIC_DATA_DIR}")

    def list_datasets(self) -> List[str]:
        return sorted(BaseSeismicRepository._datasets.keys())

    def list_section_types(self, dataset: str) -> List[str]:
        if dataset not in BaseSeismicRepository._datasets:
            available = sorted(BaseSeismicRepository._datasets.keys())
            raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")
        return BaseSeismicRepository._section_types_cache[dataset]

    def _get_base_path(self, dataset: str) -> str:
        if dataset not in BaseSeismicRepository._datasets:
            available = sorted(BaseSeismicRepository._datasets.keys())
            raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")
        return BaseSeismicRepository._datasets[dataset]
