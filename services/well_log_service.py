from repositories.well_log_repository import WellLogRepository
from dto.response.well_log_response import WellLogData
from typing import List

class WellLogService:
  def __init__(self):
    self.repository = WellLogRepository()

  def get_all_well_logs(self) -> List[WellLogData]:
    well_logs = self.repository.find_all()
    return [well_log.to_dict() for well_log in well_logs]