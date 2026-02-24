import csv
import os
from typing import List
from models.horizon_model import Horizon

class HorizonRepository:

  def __init__(self, csv_path: str = 'csv_data/horizon/horizon.csv'):
    self.csv_path = csv_path
    self._ensure_file_exists()

  def _ensure_file_exists(self):
    if not os.path.exists(self.csv_path):
      raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

  def find_all(self) -> List[Horizon]:
    horizons: List[Horizon] = []
    try:
      with open(self.csv_path, 'r', newline='') as file:
        reader = csv.DictReader(file)

        for i, row in enumerate(reader):
          try:
            horizons.append(Horizon.from_dict(row))
          except Exception as e:
            print(f"Error parsing row {i}: {e}")
            continue
    except Exception as e:
      raise Exception(f"Error reading csv file: {str(e)}")
    return horizons

  def find_all_page(self, page: int = 1, page_size: int = 500) -> List[Horizon]:
    horizons: List[Horizon] = []
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
            horizons.append(Horizon.from_dict(row))
          except Exception as e:
            print(f"Error parsing row {i}: {e}")
            continue
    except Exception as e:
      raise Exception(f"Error reading csv file: {str(e)}")
    return horizons