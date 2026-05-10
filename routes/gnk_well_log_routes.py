from flask import Blueprint
from controllers.gnk_well_log_controller import GnkWellLogController


def create_gnk_well_log_routes() -> Blueprint:
    gnk_routes = Blueprint('gnk_well_log', __name__)
    controller = GnkWellLogController()

    @gnk_routes.route('/well-log/gnk', methods=['GET'])
    def get_all():
        return controller.get_all()

    @gnk_routes.route('/well-log/gnk/wells', methods=['GET'])
    def get_well_names():
        return controller.get_well_names()

    @gnk_routes.route('/well-log/gnk/<string:well_name>', methods=['GET'])
    def get_by_well(well_name: str):
        return controller.get_by_well(well_name)

    @gnk_routes.route('/well-log/gnk/count', methods=['GET'])
    def get_count():
        return controller.get_count()

    return gnk_routes
