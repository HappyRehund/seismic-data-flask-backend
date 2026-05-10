import csv
import os
from pathlib import Path
from typing import List, Dict
from models.horizon_model import Horizon

HORIZON_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_data', 'horizon')

class HorizonRepository:

  def __init__(self):
    self._datasets: Dict[str, str] = {}
    self._cache: Dict[str, List[Horizon]] = {}
    self._discover_datasets()

  def _discover_datasets(self):
    if not os.path.isdir(HORIZON_DATA_DIR):
      raise FileNotFoundError(f"Horizon data directory not found: {HORIZON_DATA_DIR}")

    for f in sorted(os.listdir(HORIZON_DATA_DIR)):
      if f.endswith('.csv'):
        name = Path(f).stem
        self._datasets[name] = os.path.join(HORIZON_DATA_DIR, f)

    if not self._datasets:
      raise FileNotFoundError(f"No CSV files found in {HORIZON_DATA_DIR}")

  def list_datasets(self) -> List[str]:
    return sorted(self._datasets.keys())

  def _get_csv_path(self, dataset: str) -> str:
    if dataset not in self._datasets:
      available = sorted(self._datasets.keys())
      raise ValueError(f"Unknown dataset '{dataset}'. Available: {available}")
    return self._datasets[dataset]

  def _load_dataset(self, dataset: str) -> List[Horizon]:
    if dataset in self._cache:
      return self._cache[dataset]

    csv_path = self._get_csv_path(dataset)
    horizons: List[Horizon] = []

    with open(csv_path, 'r', newline='') as file:
      reader = csv.DictReader(file)
      for i, row in enumerate(reader):
        try:
          horizons.append(Horizon.from_dict(row))
        except Exception as e:
          print(f"Error parsing row {i} in {dataset}: {e}")
          continue

    self._cache[dataset] = horizons
    return horizons

  def find_all(self, dataset: str = 'horizon') -> List[Horizon]:
    return self._load_dataset(dataset)

  def find_all_page(self, dataset: str = 'horizon', page: int = 1, page_size: int = 500) -> List[Horizon]:
    all_horizons = self._load_dataset(dataset)
    start = (page - 1) * page_size
    end = start + page_size
    return all_horizons[start:end]

  def count(self, dataset: str = 'horizon') -> int:
    all_horizons = self._load_dataset(dataset)
    return len(all_horizons)

  def clear_cache(self, dataset: str | None = None):
    if dataset:
      self._cache.pop(dataset, None)
    else:
      self._cache.clear()
