from flask import Blueprint
from controllers.well_log_controller import WellLogController

def create_well_log_routes() -> Blueprint:
  well_log_routes = Blueprint('well_log', __name__)
  controller = WellLogController()

  @well_log_routes.route('/well-log', methods=['GET'])
  def get_all_well_logs():
    return controller.get_all_well_logs()

  @well_log_routes.route('/well-log/<string:well_name>', methods=['GET'])
  def get_by_well_name(well_name: str):
    return controller.get_by_well_name(well_name)

  return well_log_routes