import csv
import os
from typing import List, Optional
from models.well_log_model import WellLog

class WellLogRepository:

  def __init__(self, csv_path: str = 'csv_data/well_log/gnk_well_log.csv'):
    self.csv_path = csv_path
    self._ensure_file_exists()

  def _ensure_file_exists(self):
    if not os.path.exists(self.csv_path):
      raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

  def find_all(self) -> List[WellLog]:
    well_logs: List[WellLog] = []
    try:
      with open(self.csv_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
          try:
            well = WellLog.from_dict(row)
            well_logs.append(well)

          except Exception as e:
            print(f"Error passing row: {e}")
            continue

    except Exception as e:
      raise Exception(f"Error reading csv file: {str(e)}")

    return well_logs

  def find_by_well(self, well_name: str) -> Optional[WellLog]:
    all_well_logs = self.find_all()
    for well_log in all_well_logs:
      if well_log.well == well_name:
        return well_log
    return None

