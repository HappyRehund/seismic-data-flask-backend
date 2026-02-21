from repositories.well_log_repository import WellLogRepository
from models.well_log_model import WellLog
from typing import List

class WellLogService:
  def __init__(self):
    self.repository = WellLogRepository()

  def get_all_well_logs(self) -> List[WellLog]:
    return self.repository.find_all()