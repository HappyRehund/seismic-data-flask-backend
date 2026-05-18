from services.well_log_service import WellLogService
from typing import Tuple
from flask import Response, request, jsonify
from common.response_utils import success_response, error_response, ListResponse
from models.well_log_model import WellLogStats, WellLogWellStats


class WellLogController:
    def __init__(self):
        self.service = WellLogService()

    def get_all_by_type(self, log_type: str) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'default')
            well_logs = self.service.get_all_by_type(log_type, dataset=dataset)
            return success_response(ListResponse("wells", well_logs))
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_by_well_name(self, log_type: str, well_name: str) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'default')
            well_log = self.service.get_by_well_name(log_type, well_name, dataset=dataset)
            if well_log is None:
                return error_response(f"Well '{well_name}' not found in {log_type.upper()} log (dataset: '{dataset}')", 404)
            return success_response(well_log)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_well_names(self, log_type: str) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'default')
            names = self.service.get_well_names(log_type, dataset=dataset)
            return success_response(ListResponse("well_names", names))
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_datasets(self) -> Tuple[Response, int]:
        try:
            datasets = self.service.get_available_datasets()
            result = {}
            for ds in datasets:
                log_types = self.service.get_log_types(ds)
                result[ds] = log_types
            return jsonify({
                "success": True,
                "data": {"datasets": result, "count": len(datasets)}
            }), 200
        except Exception as e:
            return error_response(str(e), 500)

    def get_stats(self, log_type: str) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'default')
            stats = self.service.get_stats(log_type, dataset=dataset)
            return success_response(stats)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    def get_well_stats(self, log_type: str, well_name: str) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'default')
            stats = self.service.get_well_stats(log_type, well_name, dataset=dataset)
            if stats is None:
                return error_response(f"Well '{well_name}' not found in {log_type.upper()} log (dataset: '{dataset}')", 404)
            return success_response(stats)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
