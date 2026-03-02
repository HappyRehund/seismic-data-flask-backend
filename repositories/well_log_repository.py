import csv
import os
from typing import List, Optional, Dict
from models.well_log_model import WellLogEntry, WellLogData


class WellLogType:
  PHIE = "phie"
  SWE = "swe"
  VSH = "vsh"

  VALID_TYPES = [PHIE, SWE, VSH]

  CSV_MAP: Dict[str, str] = {
    PHIE: "csv_data/well_log/phie/PHIE.csv",
    SWE: "csv_data/well_log/swe/SWE.csv",
    VSH: "csv_data/well_log/vsh/VSH.csv",
  }


class WellLogRepository:

  def __init__(self):
    for log_type, path in WellLogType.CSV_MAP.items():
      if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found for {log_type}: {path}")

  def _get_csv_path(self, log_type: str) -> str:
    if log_type not in WellLogType.CSV_MAP:
      raise ValueError(f"Invalid log type: {log_type}. Valid types: {WellLogType.VALID_TYPES}")
    return WellLogType.CSV_MAP[log_type]

  def get_well_names(self, log_type: str) -> List[str]:
    csv_path = self._get_csv_path(log_type)
    try:
      with open(csv_path, 'r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        return [h.strip() for h in headers[1:]]
    except Exception as e:
      raise Exception(f"Error reading CSV file: {str(e)}")

  def find_all(self, log_type: str) -> List[WellLogData]:
    csv_path = self._get_csv_path(log_type)
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

    return result

  def find_by_well_name(self, log_type: str, well_name: str) -> Optional[WellLogData]:
    csv_path = self._get_csv_path(log_type)
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
