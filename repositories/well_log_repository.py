import csv
import os
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from models.well_log_model import WellLogEntry, WellLogData

WELL_LOG_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'well_log')

LOG_TYPE_FILES: Dict[str, str] = {
    "phie": "PHIE.csv",
    "swe": "SWE.csv",
    "vsh": "VSH.csv",
}


class WellLogRepository:

    def __init__(self):
        self._datasets: Dict[str, str] = {}
        self._log_types_cache: Dict[str, List[str]] = {}
        self._cache: Dict[Tuple[str, str], List[WellLogData]] = {}
        self._discover_datasets()

    def _discover_datasets(self):
        if not os.path.isdir(WELL_LOG_DATA_DIR):
            raise FileNotFoundError(f"Well log data directory not found: {WELL_LOG_DATA_DIR}")

        for entry in sorted(os.listdir(WELL_LOG_DATA_DIR)):
            full_path = os.path.join(WELL_LOG_DATA_DIR, entry)
            if os.path.isdir(full_path):
                available_types = []
                for log_type, filename in LOG_TYPE_FILES.items():
                    candidate = os.path.join(full_path, log_type, filename)
                    if os.path.exists(candidate):
                        available_types.append(log_type)
                if available_types:
                    self._datasets[entry] = full_path
                    self._log_types_cache[entry] = sorted(available_types)

        if not self._datasets:
            raise FileNotFoundError(f"No well log datasets found in {WELL_LOG_DATA_DIR}")

    def list_datasets(self) -> List[str]:
        return sorted(self._datasets.keys())

    def list_log_types(self, dataset: str) -> List[str]:
        if dataset not in self._datasets:
            available = sorted(self._datasets.keys())
            raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")
        return self._log_types_cache[dataset]

    def _get_csv_path(self, log_type: str, dataset: str = 'default') -> str:
        if dataset not in self._datasets:
            available = sorted(self._datasets.keys())
            raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")

        if log_type not in LOG_TYPE_FILES:
            raise ValueError(f"Invalid log type: {log_type}. Valid types: {list(LOG_TYPE_FILES.keys())}")

        return os.path.join(self._datasets[dataset], log_type, LOG_TYPE_FILES[log_type])

    def _validate_log_type(self, log_type: str) -> str:
        log_type = log_type.lower()
        if log_type not in LOG_TYPE_FILES:
            raise ValueError(f"Invalid log type: '{log_type}'. Valid types: {list(LOG_TYPE_FILES.keys())}")
        return log_type

    def get_well_names(self, log_type: str, dataset: str = 'default') -> List[str]:
        log_type = self._validate_log_type(log_type)
        csv_path = self._get_csv_path(log_type, dataset)
        try:
            with open(csv_path, 'r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)
                return [h.strip() for h in headers[1:]]
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

    def find_all(self, log_type: str, dataset: str = 'default') -> List[WellLogData]:
        log_type = self._validate_log_type(log_type)
        cache_key = (dataset, log_type)
        if cache_key in self._cache:
            return self._cache[cache_key]

        csv_path = self._get_csv_path(log_type, dataset)
        well_names: List[str] = []
        well_entries: Dict[str, List[WellLogEntry]] = {}

        try:
            with open(csv_path, 'r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)
                well_names = [h.strip() for h in headers[1:]]

                for name in well_names:
                    well_entries[name] = []

                for row in reader:
                    try:
                        twt = float(row[0])
                    except (ValueError, IndexError):
                        continue

                    for idx, name in enumerate(well_names):
                        col_idx = idx + 1
                        raw_value = row[col_idx] if col_idx < len(row) else ''
                        entry = WellLogEntry.from_dict(twt, raw_value)
                        well_entries[name].append(entry)

        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

        result: List[WellLogData] = []
        for name in well_names:
            result.append(WellLogData(
                well_name=name,
                log_type=log_type,
                entries=well_entries[name]
            ))

        self._cache[cache_key] = result
        return result

    def find_by_well_name(self, log_type: str, well_name: str, dataset: str = 'default') -> Optional[WellLogData]:
        log_type = self._validate_log_type(log_type)
        csv_path = self._get_csv_path(log_type, dataset)
        entries: List[WellLogEntry] = []
        col_index: Optional[int] = None

        try:
            with open(csv_path, 'r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)
                header_names = [h.strip() for h in headers]

                for idx, name in enumerate(header_names):
                    if name == well_name:
                        col_index = idx
                        break

                if col_index is None:
                    return None

                for row in reader:
                    try:
                        twt = float(row[0])
                    except (ValueError, IndexError):
                        continue

                    raw_value = row[col_index] if col_index < len(row) else ''
                    entries.append(WellLogEntry.from_dict(twt, raw_value))

        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

        return WellLogData(
            well_name=well_name,
            log_type=log_type,
            entries=entries
        )

    def clear_cache(self, dataset: str | None = None, log_type: str | None = None):
        if dataset and log_type:
            self._cache.pop((dataset, log_type), None)
        elif dataset:
            keys_to_remove = [k for k in self._cache if k[0] == dataset]
            for k in keys_to_remove:
                self._cache.pop(k)
        else:
            self._cache.clear()
