from flask import Response
from typing import Tuple

from common.response_utils import error_response, success_response
from services.image_helper_service import ImageHelperService


class ImageHelperController:
    def __init__(self):
        self.service = ImageHelperService()

    def get_image_dimensions(self, section_type: str, number: int) -> Tuple[Response, int]:
        try:
            dimensions = self.service.get_image_dimensions(section_type, number)
            if dimensions is None:
                return error_response(
                    f"Image for {section_type} {number} not found",
                    404,
                )

            return success_response(dimensions)
        except ValueError as error:
            return error_response(str(error), 400)
        except Exception as error:
            return error_response(str(error), 500)