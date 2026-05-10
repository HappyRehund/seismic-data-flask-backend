from flask import Response, request, jsonify
from typing import Tuple

from common.response_utils import error_response, success_response
from services.image_helper_service import ImageHelperService


class ImageHelperController:
    def __init__(self):
        self.service = ImageHelperService()

    def get_image_dimensions(self, section_type: str, number: int) -> Tuple[Response, int]:
        try:
            dataset = request.args.get('dataset', 'default')
            dimensions = self.service.get_image_dimensions(section_type, number, dataset=dataset)
            if dimensions is None:
                return error_response(
                    f"Image for {section_type} {number} not found in dataset '{dataset}'",
                    404,
                )

            return success_response(dimensions)
        except ValueError as error:
            return error_response(str(error), 400)
        except Exception as error:
            return error_response(str(error), 500)

    def get_datasets(self) -> Tuple[Response, int]:
        try:
            datasets = self.service.get_available_datasets()
            result = {}
            for ds in datasets:
                section_types = self.service.get_section_types(ds)
                result[ds] = section_types
            return jsonify({
                "success": True,
                "data": {"datasets": result, "count": len(datasets)}
            }), 200
        except Exception as error:
            return error_response(str(error), 500)
