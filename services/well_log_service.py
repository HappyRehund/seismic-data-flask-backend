from typing import List, Optional
from repositories.well_log_repository import WellLogRepository, WellLogType
from models.well_log_model import WellLogData


class WellLogService:
  def __init__(self):
    self.repository = WellLogRepository()

  def _validate_log_type(self, log_type: str) -> str:
    log_type = log_type.lower()
    if log_type not in WellLogType.VALID_TYPES:
      raise ValueError(f"Invalid log type: '{log_type}'. Valid types: {WellLogType.VALID_TYPES}")
    return log_type

  def get_all_by_type(self, log_type: str) -> List[WellLogData]:
    log_type = self._validate_log_type(log_type)
    return self.repository.find_all(log_type)

  def get_by_well_name(self, log_type: str, well_name: str) -> Optional[WellLogData]:
    log_type = self._validate_log_type(log_type)
    if not well_name:
      raise ValueError("Well name is required")
    return self.repository.find_by_well_name(log_type, well_name)

  def get_well_names(self, log_type: str) -> List[str]:
    log_type = self._validate_log_type(log_type)
    return self.repository.get_well_names(log_type)
