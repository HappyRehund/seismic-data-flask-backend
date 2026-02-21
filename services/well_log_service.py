from repositories.well_log_repository import WellLogRepository
from models.well_log_model import WellLog
from typing import List

class WellLogService:
  def __init__(self):
    self.repository = WellLogRepository()

  def get_all_well_logs(self, page: int = 1, page_size: int = 500) -> List[WellLog]:
    return self.repository.find_all(page=page, page_size=page_size)

  def get_by_well_name(self, well_name: str) -> List[WellLog]:
    return self.repository.find_by_well(well_name)

  def count(self) -> int:
    return self.repository.count()