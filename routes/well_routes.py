from flask import Blueprint
from controllers.well_controller import WellController


def create_well_routes() -> Blueprint:
    well_routes = Blueprint('well', __name__)
    controller = WellController()

    @well_routes.route('/well', methods=['GET'])
    def get_all_wells():
        return controller.get_all_wells()

    @well_routes.route('/well/summary', methods=['GET'])
    def get_wells_summary():
        return controller.get_wells_summary()

    @well_routes.route('/well/<string:well_name>', methods=['GET'])
    def get_well_by_name(well_name: str):
        return controller.get_well_by_name(well_name)

    @well_routes.route('/well/<string:well_name>/exists', methods=['GET'])
    def check_well_exists(well_name: str):
        return controller.check_well_exists(well_name)

    return well_routes
