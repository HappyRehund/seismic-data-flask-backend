from flask import Response
from typing import Tuple
from services.well_service import WellService
from common.response_utils import success_response, error_response
from dto.base import ListResponse
from dto.response.well_response import WellsSummaryResponse, WellExistsResponse

class WellController:
    def __init__(self):
        self.service = WellService()

    def get_all_wells(self) -> Tuple[Response, int]:
        try:
            wells = self.service.get_all_wells()
            return success_response(ListResponse("wells", wells))
        except Exception as e:
            return error_response(str(e), 500)

    def get_well_by_name(self, well_name: str) -> Tuple[Response, int]:
        try:
            well = self.service.get_well_by_name(well_name)
            if well is None:
                return error_response(f"Well '{well_name}' not found", 404)
            return success_response(well)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_wells_summary(self) -> Tuple[Response, int]:
        try:
            summary_data = self.service.get_wells_summary()
            response = WellsSummaryResponse.from_dict(summary_data)
            return success_response(response)
        except Exception as e:
            return error_response(str(e), 500)

    def check_well_exists(self, well_name: str) -> Tuple[Response, int]:
        try:
            exists = self.service.check_well_exists(well_name)
            response = WellExistsResponse(exists=exists)
            return success_response(response)
        except Exception as e:
            return error_response(str(e), 500)
