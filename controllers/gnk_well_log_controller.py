from services.gnk_well_log_service import GnkWellLogService
from typing import Tuple
from flask import Response, request, jsonify
from common.response_utils import success_response, error_response, ListResponse


class GnkWellLogController:
    def __init__(self):
        self.service = GnkWellLogService()

    def get_all(self) -> Tuple[Response, int]:
        try:
            entries = self.service.get_all()
            return success_response(ListResponse("entries", entries))
        except Exception as e:
            return error_response(str(e), 500)

    def get_by_well(self, well_name: str) -> Tuple[Response, int]:
        try:
            entries = self.service.get_by_well(well_name)
            if not entries:
                return error_response(f"Well '{well_name}' not found in GNK well log", 404)
            return success_response(ListResponse("entries", entries))
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_well_names(self) -> Tuple[Response, int]:
        try:
            names = self.service.get_well_names()
            return success_response(ListResponse("well_names", names))
        except Exception as e:
            return error_response(str(e), 500)

    def get_count(self) -> Tuple[Response, int]:
        try:
            count = self.service.count()
            return jsonify({
                "success": True,
                "data": {"total_entries": count}
            }), 200
        except Exception as e:
            return error_response(str(e), 500)
