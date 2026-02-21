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
      with open(self.csv_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
          try:
            horizon = Horizon.from_dict(row)
            horizons.append(horizon)

          except Exception as e:
            print(f"Error passing row: {e}")
            continue

    except Exception as e:
      raise Exception(f"Error reading csv file: {str(e)}")

    return horizons