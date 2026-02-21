from services.well_log_service import WellLogService
from typing import Tuple
from flask import Response
from common.response_utils import error_response, success_response
from dto.base import ListResponse

class WellLogController:
  def __init__(self):
    self.service = WellLogService()

  def get_all_wells(self) -> Tuple[Response, int]:
    try:
      well_logs = self.service.get_all_well_logs()
      return success_response(ListResponse("well_logs", well_logs))

    except Exception as e:
      return error_response(str(e), 500)