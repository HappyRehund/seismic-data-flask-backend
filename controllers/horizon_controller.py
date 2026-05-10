from services.horizon_service import HorizonService
from typing import Tuple
from flask import Response, request, jsonify
from common.response_utils import success_response, error_response, ListResponse

class HorizonController:
  def __init__(self):
    self.service = HorizonService()

  def get_all_horizons(self) -> Tuple[Response, int]:
    try:
      dataset = request.args.get('dataset', 'horizon')
      horizons = self.service.get_all_horizons(dataset=dataset)
      return success_response(ListResponse("horizons", horizons))

    except Exception as e:
      return error_response(str(e), 500)

  def get_all_horizons_page(self) -> Tuple[Response, int]:
    try:
      dataset = request.args.get('dataset', 'horizon')
      page = int(request.args.get('page', 1))
      page_size = int(request.args.get('page_size', 500))
      horizons = self.service.get_all_horizons_page(dataset=dataset, page=page, page_size=page_size)
      return success_response(ListResponse("horizons", horizons))
    except Exception as e:
      return error_response(str(e), 500)

  def get_datasets(self) -> Tuple[Response, int]:
    try:
      datasets = self.service.get_available_datasets()
      return jsonify({
        "success": True,
        "data": {"datasets": datasets, "count": len(datasets)}
      }), 200
    except Exception as e:
      return error_response(str(e), 500)
