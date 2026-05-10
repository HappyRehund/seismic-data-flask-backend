import csv
import os
from typing import List, Optional, Dict
from models.gnk_well_log_model import GnkWellLogEntry

GNK_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'well_log', 'gnk', 'gnk_well_log.csv')


class GnkWellLogRepository:
    def __init__(self):
        self._cache: List[GnkWellLogEntry] = []
        self._well_names_cache: List[str] = []
        self._loaded = False

    def _load_data(self) -> List[GnkWellLogEntry]:
        if self._loaded:
            return self._cache

        if not os.path.exists(GNK_CSV_PATH):
            raise FileNotFoundError(f"GNK well log CSV not found: {GNK_CSV_PATH}")

        entries: List[GnkWellLogEntry] = []
        well_names: set[str] = set()

        with open(GNK_CSV_PATH, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                try:
                    entry = GnkWellLogEntry.from_dict(row)
                    entries.append(entry)
                    if entry.well:
                        well_names.add(entry.well)
                except Exception as e:
                    print(f"Error parsing GNK well log row {i}: {e}")
                    continue

        self._cache = entries
        self._well_names_cache = sorted(well_names)
        self._loaded = True
        return entries

    def find_all(self) -> List[GnkWellLogEntry]:
        return self._load_data()

    def find_by_well(self, well_name: str) -> List[GnkWellLogEntry]:
        all_entries = self._load_data()
        return [e for e in all_entries if e.well == well_name]

    def get_well_names(self) -> List[str]:
        self._load_data()
        return self._well_names_cache

    def count(self) -> int:
        return len(self._load_data())

    def clear_cache(self):
        self._cache.clear()
        self._well_names_cache.clear()
        self._loaded = False
