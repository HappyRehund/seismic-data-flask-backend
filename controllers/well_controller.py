from flask import Response
from typing import Tuple
from services.well_service import WellService
from common.response_utils import success_response, error_response
from dto.well_response import (
    WellResponse,
    WellsListResponse,
    WellsSummaryResponse,
    WellExistsResponse
)

class WellController:
    def __init__(self):
        self.service = WellService()

    def get_all_wells(self) -> Tuple[Response, int]:
        """
        GET /wells
        Returns a list of all wells with count
        """
        try:
            wells_data = self.service.get_all_wells()
            response = WellsListResponse.from_well_dicts(wells_data)
            return success_response(response)
        except Exception as e:
            return error_response(str(e), 500)

    def get_well_by_name(self, well_name: str) -> Tuple[Response, int]:
        """
        GET /wells/:name
        Returns detailed information about a specific well
        """
        try:
            well_data = self.service.get_well_by_name(well_name)
            if well_data is None:
                return error_response(f"Well '{well_name}' not found", 404)
            response = WellResponse(**well_data)
            return success_response(response)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_wells_summary(self) -> Tuple[Response, int]:
        """
        GET /wells/summary
        Returns summary statistics for all wells including total count,
        inline/crossline ranges, and list of well names
        """
        try:
            summary_data = self.service.get_wells_summary()
            response = WellsSummaryResponse.from_dict(summary_data)
            return success_response(response)
        except Exception as e:
            return error_response(str(e), 500)

    def check_well_exists(self, well_name: str) -> Tuple[Response, int]:
        """
        GET /wells/:name/exists
        Checks if a well with the given name exists
        """
        try:
            exists = self.service.check_well_exists(well_name)
            response = WellExistsResponse(exists=exists)
            return success_response(response)
        except Exception as e:
            return error_response(str(e), 500)
