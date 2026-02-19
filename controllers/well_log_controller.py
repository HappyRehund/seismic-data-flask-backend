from services.well_log_service import WellLogService
from typing import Tuple
from flask import Response
from common.response_utils import error_response, success_response
from dto.response.well_log_response import WellLogResponse, WellLogsResponse

class WellLogController:
  def __init__(self):
    self.service = WellLogService()
    self.service.get_all_well_logs

  def get_all_wells(self) -> Tuple[Response, int]:
    try:
      well_logs_data = self.service.get_all_well_logs()
      response =  WellLogsResponse.from_well_log_dicts(well_logs_data)
      return success_response(response)

    except Exception as e:
      return error_response(str(e), 500)