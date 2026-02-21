from services.well_log_service import WellLogService
from typing import Tuple
from flask import Response, request
from common.response_utils import error_response, success_response
from dto.base import ListResponse

class WellLogController:
  def __init__(self):
    self.service = WellLogService()

  def get_all_well_logs(self) -> Tuple[Response, int]:
    try:
      page = int(request.args.get('page', 1))
      page_size = int(request.args.get('page_size', 500))
      well_logs = self.service.get_all_well_logs(page=page, page_size=page_size)
      return success_response(ListResponse("well_logs", well_logs))
    except Exception as e:
      return error_response(str(e), 500)

  def get_by_well_name(self, well_name: str) -> Tuple[Response, int]:
    try:
      well_logs = self.service.get_by_well_name(well_name)
      if not well_logs:
        return error_response(f"No well logs found for '{well_name}'", 404)
      return success_response(ListResponse("well_logs", well_logs))
    except Exception as e:
      return error_response(str(e), 500)