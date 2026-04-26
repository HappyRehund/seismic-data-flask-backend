from flask import Blueprint

from controllers.image_helper_controller import ImageHelperController


def create_image_helper_routes() -> Blueprint:
    image_helper_routes = Blueprint('image_helper', __name__)
    controller = ImageHelperController()

    @image_helper_routes.route('/image-helper/<section_type>/<int:number>/dimensions', methods=['GET'])
    def get_image_dimensions(section_type: str, number: int):
        return controller.get_image_dimensions(section_type, number)

    return image_helper_routes