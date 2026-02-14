from flask import request, Response
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

    def search_wells_by_inline(self) -> Tuple[Response, int]:
        """
        GET /wells/search/inline?min=X&max=Y
        Returns wells within the specified inline range
        """
        try:
            min_inline = request.args.get('min', type=int)
            max_inline = request.args.get('max', type=int)

            if min_inline is None or max_inline is None:
                return error_response("Both 'min' and 'max' query parameters are required", 400)

            wells_data = self.service.search_wells_by_inline(min_inline, max_inline)
            response = WellsListResponse.from_well_dicts(wells_data)
            return success_response(response)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def search_wells_by_crossline(self) -> Tuple[Response, int]:
        """
        GET /wells/search/crossline?min=X&max=Y
        Returns wells within the specified crossline range
        """
        try:
            min_crossline = request.args.get('min', type=int)
            max_crossline = request.args.get('max', type=int)

            if min_crossline is None or max_crossline is None:
                return error_response("Both 'min' and 'max' query parameters are required", 400)

            wells_data = self.service.search_wells_by_crossline(min_crossline, max_crossline)
            response = WellsListResponse.from_well_dicts(wells_data)
            return success_response(response)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def search_wells_by_area(self) -> Tuple[Response, int]:
        """
        GET /wells/search/area?min_inline=X&max_inline=Y&min_crossline=A&max_crossline=B
        Returns wells within the specified rectangular area defined by inline and crossline ranges
        """
        try:
            min_inline = request.args.get('min_inline', type=int)
            max_inline = request.args.get('max_inline', type=int)
            min_crossline = request.args.get('min_crossline', type=int)
            max_crossline = request.args.get('max_crossline', type=int)

            if min_inline is None or max_inline is None or min_crossline is None or max_crossline is None:
                return error_response(
                    "All parameters required: min_inline, max_inline, min_crossline, max_crossline",
                    400
                )

            wells_data = self.service.get_wells_in_area(
                min_inline, max_inline, min_crossline, max_crossline
            )
            response = WellsListResponse.from_well_dicts(wells_data)
            return success_response(response)
        except ValueError as e:
            return error_response(str(e), 400)
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
