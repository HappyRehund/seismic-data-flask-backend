import csv
import os
from pathlib import Path
from typing import List, Optional, Dict
from models.well_model import WellCoordinate

WELL_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'well')


class WellRepository:
    def __init__(self):
        self._datasets: Dict[str, str] = {}
        self._cache: Dict[str, List[WellCoordinate]] = {}
        self._discover_datasets()

    def _discover_datasets(self):
        if not os.path.isdir(WELL_DATA_DIR):
            raise FileNotFoundError(f"Well data directory not found: {WELL_DATA_DIR}")

        for f in sorted(os.listdir(WELL_DATA_DIR)):
            if f.endswith('.csv'):
                name = Path(f).stem
                self._datasets[name] = os.path.join(WELL_DATA_DIR, f)

        if not self._datasets:
            raise FileNotFoundError(f"No CSV files found in {WELL_DATA_DIR}")

    def list_datasets(self) -> List[str]:
        return sorted(self._datasets.keys())

    def _get_csv_path(self, dataset: str) -> str:
        if dataset not in self._datasets:
            available = sorted(self._datasets.keys())
            raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")
        return self._datasets[dataset]

    def _load_dataset(self, dataset: str) -> List[WellCoordinate]:
        if dataset in self._cache:
            return self._cache[dataset]

        csv_path = self._get_csv_path(dataset)
        wells: List[WellCoordinate] = []

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                try:
                    well = WellCoordinate.from_dict(row)
                    wells.append(well)
                except ValueError as e:
                    print(f"Error parsing row in {dataset}: {e}")
                    continue

        self._cache[dataset] = wells
        return wells

    def find_all(self, dataset: str = 'well_coordinatesmj_B_G') -> List[WellCoordinate]:
        return self._load_dataset(dataset)

    def find_by_name(self, well_name: str, dataset: str = 'well_coordinatesmj_B_G') -> Optional[WellCoordinate]:
        all_wells = self._load_dataset(dataset)
        for well in all_wells:
            if well.well_name == well_name:
                return well
        return None

    def count(self, dataset: str = 'well_coordinatesmj_B_G') -> int:
        return len(self._load_dataset(dataset))

    def exists(self, well_name: str, dataset: str = 'well_coordinatesmj_B_G') -> bool:
        return self.find_by_name(well_name, dataset=dataset) is not None

    def clear_cache(self, dataset: str | None = None):
        if dataset:
            self._cache.pop(dataset, None)
        else:
            self._cache.clear()
