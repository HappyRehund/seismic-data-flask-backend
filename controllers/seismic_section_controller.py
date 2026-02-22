from services.seismic_section_service import SeismicSectionService
from typing import Tuple
from flask import Response
from common.response_utils import file_response, error_response


class SeismicSectionController:
    def __init__(self):
        self.service = SeismicSectionService()

    def get_inline_image(self, number: int) -> Tuple[Response, int] | Response:
        """Return a PNG image for the requested inline section number."""
        try:
            section = self.service.get_inline_image(number)
            if section is None:
                return error_response(f"Inline section {number} not found", 404)

            return file_response(
                data=section.image_data,
                mime_type='image/png',
                filename=f'inline_{number}.png',
            )
        except Exception as e:
            return error_response(str(e), 500)

    def get_crossline_image(self, number: int) -> Tuple[Response, int] | Response:
        """Return a PNG image for the requested crossline section number."""
        try:
            section = self.service.get_crossline_image(number)
            if section is None:
                return error_response(f"Crossline section {number} not found", 404)

            return file_response(
                data=section.image_data,
                mime_type='image/png',
                filename=f'crossline_{number}.png',
            )
        except Exception as e:
            return error_response(str(e), 500)
