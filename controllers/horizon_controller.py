from services.horizon_service import HorizonService
from typing import Tuple
from flask import Response
from common.response_utils import success_response, error_response
from dto.base import ListResponse

class HorizonController:
  def __init__(self):
    self.service = HorizonService()

  def get_all_horizons(self) -> Tuple[Response, int]:
    try:
      horizons = self.service.get_all_horizons()
      return success_response(ListResponse("horizons", horizons))
    except Exception as e:
      return error_response(str(e), 500)
