from flask import Blueprint
from controllers.seismic_section_controller import SeismicSectionController


def create_seismic_section_routes() -> Blueprint:
    seismic_routes = Blueprint('seismic_section', __name__)
    controller = SeismicSectionController()

    @seismic_routes.route('/inline/<int:number>/image', methods=['GET'])
    def get_inline_image(number: int):
        return controller.get_inline_image(number)

    @seismic_routes.route('/crossline/<int:number>/image', methods=['GET'])
    def get_crossline_image(number: int):
        return controller.get_crossline_image(number)

    return seismic_routes
