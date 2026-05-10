from flask import Response, request, jsonify
from typing import Tuple
from services.well_service import WellService
from common.response_utils import success_response, error_response, ListResponse
from models.well_model import WellsSummaryResponse, WellExistsResponse

class WellController:
    def __init__(self):
        self.service = WellService()

    def get_all_wells(self) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'well_coordinatesmj_B_G')
            wells = self.service.get_all_wells(dataset=dataset)
            return success_response(ListResponse("wells", wells))
        except Exception as e:
            return error_response(str(e), 500)

    def get_well_by_name(self, well_name: str) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'well_coordinatesmj_B_G')
            well = self.service.get_well_by_name(well_name, dataset=dataset)
            if well is None:
                return error_response(f"Well '{well_name}' not found in dataset '{dataset}'", 404)
            return success_response(well)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_wells_summary(self) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'well_coordinatesmj_B_G')
            summary_data = self.service.get_wells_summary(dataset=dataset)
            response = WellsSummaryResponse.from_dict(summary_data)
            return success_response(response)
        except Exception as e:
            return error_response(str(e), 500)

    def check_well_exists(self, well_name: str) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'well_coordinatesmj_B_G')
            exists = self.service.check_well_exists(well_name, dataset=dataset)
            response = WellExistsResponse(exists=exists)
            return success_response(response)
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
