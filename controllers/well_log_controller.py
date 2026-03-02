from services.well_log_service import WellLogService
from typing import Tuple
from flask import Response
from common.response_utils import success_response, error_response, ListResponse


class WellLogController:
  def __init__(self):
    self.service = WellLogService()

  def get_all_by_type(self, log_type: str) -> Tuple[Response, int]:
    try:
      well_logs = self.service.get_all_by_type(log_type)
      return success_response(ListResponse("wells", well_logs))
    except ValueError as e:
      return error_response(str(e), 400)
    except Exception as e:
      return error_response(str(e), 500)

  def get_by_well_name(self, log_type: str, well_name: str) -> Tuple[Response, int]:
    try:
      well_log = self.service.get_by_well_name(log_type, well_name)
      if well_log is None:
        return error_response(f"Well '{well_name}' not found in {log_type.upper()} log", 404)
      return success_response(well_log)
    except ValueError as e:
      return error_response(str(e), 400)
    except Exception as e:
      return error_response(str(e), 500)

  def get_well_names(self, log_type: str) -> Tuple[Response, int]:
    try:
      names = self.service.get_well_names(log_type)
      return success_response(ListResponse("well_names", names))
    except ValueError as e:
      return error_response(str(e), 400)
    except Exception as e:
      return error_response(str(e), 500)
