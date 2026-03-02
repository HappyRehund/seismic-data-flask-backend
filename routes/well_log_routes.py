from flask import Blueprint
from controllers.well_log_controller import WellLogController


def create_well_log_routes() -> Blueprint:
    well_log_routes = Blueprint('well_log', __name__)
    controller = WellLogController()

    # --- PHIE endpoints ---
    @well_log_routes.route('/well-log/phie', methods=['GET'])
    def get_all_phie():
        return controller.get_all_by_type('phie')

    @well_log_routes.route('/well-log/phie/wells', methods=['GET'])
    def get_phie_well_names():
        return controller.get_well_names('phie')

    @well_log_routes.route('/well-log/phie/<string:well_name>', methods=['GET'])
    def get_phie_by_well(well_name: str):
        return controller.get_by_well_name('phie', well_name)

    # --- SWE endpoints ---
    @well_log_routes.route('/well-log/swe', methods=['GET'])
    def get_all_swe():
        return controller.get_all_by_type('swe')

    @well_log_routes.route('/well-log/swe/wells', methods=['GET'])
    def get_swe_well_names():
        return controller.get_well_names('swe')

    @well_log_routes.route('/well-log/swe/<string:well_name>', methods=['GET'])
    def get_swe_by_well(well_name: str):
        return controller.get_by_well_name('swe', well_name)

    # --- VSH endpoints ---
    @well_log_routes.route('/well-log/vsh', methods=['GET'])
    def get_all_vsh():
        return controller.get_all_by_type('vsh')

    @well_log_routes.route('/well-log/vsh/wells', methods=['GET'])
    def get_vsh_well_names():
        return controller.get_well_names('vsh')

    @well_log_routes.route('/well-log/vsh/<string:well_name>', methods=['GET'])
    def get_vsh_by_well(well_name: str):
        return controller.get_by_well_name('vsh', well_name)

    return well_log_routes
