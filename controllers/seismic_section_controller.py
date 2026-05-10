from services.seismic_section_service import SeismicSectionService
from typing import Tuple
from flask import Response, request, jsonify
from common.response_utils import file_response, error_response


class SeismicSectionController:
    def __init__(self):
        self.service = SeismicSectionService()

    def get_inline_image(self, number: int) -> Tuple[Response, int] | Response:
        """Return a PNG image for the requested inline section number."""
        try:
            dataset = request.args.get('dataset', 'default')
            section = self.service.get_inline_image(number, dataset=dataset)
            if section is None:
                return error_response(f"Inline section {number} not found in dataset '{dataset}'", 404)

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
            dataset = request.args.get('dataset', 'default')
            section = self.service.get_crossline_image(number, dataset=dataset)
            if section is None:
                return error_response(f"Crossline section {number} not found in dataset '{dataset}'", 404)

            return file_response(
                data=section.image_data,
                mime_type='image/png',
                filename=f'crossline_{number}.png',
            )
        except Exception as e:
            return error_response(str(e), 500)

    def get_inline_mjb_image(self, number: int) -> Tuple[Response, int] | Response:
        """Return a PNG image for the requested inline MJB section number."""
        try:
            dataset = request.args.get('dataset', 'default')
            section = self.service.get_inline_mjb_image(number, dataset=dataset)
            if section is None:
                return error_response(f"Inline MJB section {number} not found in dataset '{dataset}'", 404)

            return file_response(
                data=section.image_data,
                mime_type='image/png',
                filename=f'inlineMJB_{number}.png',
            )
        except Exception as e:
            return error_response(str(e), 500)

    def get_crossline_mjb_image(self, number: int) -> Tuple[Response, int] | Response:
        """Return a PNG image for the requested crossline MJB section number."""
        try:
            dataset = request.args.get('dataset', 'default')
            section = self.service.get_crossline_mjb_image(number, dataset=dataset)
            if section is None:
                return error_response(f"Crossline MJB section {number} not found in dataset '{dataset}'", 404)

            return file_response(
                data=section.image_data,
                mime_type='image/png',
                filename=f'crosslineMJB_{number}.png',
            )
        except Exception as e:
            return error_response(str(e), 500)

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
        except Exception as e:
            return error_response(str(e), 500)
