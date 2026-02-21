from services.horizon_service import HorizonService
from typing import Tuple
from flask import Response, request
from common.response_utils import success_response, error_response
from dto.base import ListResponse

class HorizonController:
  def __init__(self):
    self.service = HorizonService()

  def get_all_horizons(self) -> Tuple[Response, int]:
    try:
      page = int(request.args.get('page', 1))
      page_size = int(request.args.get('page_size', 500))
      horizons = self.service.get_all_horizons(page=page, page_size=page_size)
      return success_response(ListResponse("horizons", horizons))
    except Exception as e:
      return error_response(str(e), 500)
