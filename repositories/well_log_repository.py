import csv
import os
from typing import List, Optional
from models.well_log_model import WellLog
from common.well_name_utils import normalize_well_name

class WellLogRepository:

  def __init__(self, csv_path: str = 'csv_data/well_log/gnk_well_log.csv'):
    self.csv_path = csv_path
    self._ensure_file_exists()

  def _ensure_file_exists(self):
    if not os.path.exists(self.csv_path):
      raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

  def find_all(self, page: int = 1, page_size: int = 500) -> List[WellLog]:
    well_logs: List[WellLog] = []
    start = (page - 1) * page_size
    end = start + page_size
    try:
      with open(self.csv_path, 'r', newline='') as file:
        reader = csv.DictReader(file)  # comma-delimited (default)
        for i, row in enumerate(reader):
          if i < start:
            continue
          if i >= end:
            break
          try:
            well_logs.append(WellLog.from_dict(row))
          except Exception as e:
            print(f"Error parsing row {i}: {e}")
            continue
    except Exception as e:
      raise Exception(f"Error reading csv file: {str(e)}")
    return well_logs

  def find_by_well(self, well_name: str) -> List[WellLog]:
    """Return all rows for a well, normalizing the name before comparison."""
    canonical = normalize_well_name(well_name)
    results: List[WellLog] = []
    try:
      with open(self.csv_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
          if normalize_well_name(row.get('WELL', '')) == canonical:
            try:
              results.append(WellLog.from_dict(row))
            except Exception as e:
              print(f"Error parsing row: {e}")
    except Exception as e:
      raise Exception(f"Error reading csv file: {str(e)}")
    return results

  def count(self) -> int:
    try:
      with open(self.csv_path, 'r', newline='') as file:
        return sum(1 for _ in file) - 1  # minus header
    except Exception as e:
      raise Exception(f"Error reading csv file: {str(e)}")

