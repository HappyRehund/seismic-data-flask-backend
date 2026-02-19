from flask import Blueprint
from controllers.well_log_controller import WellLogController

def create_well_log_routes() -> Blueprint:
  well_log_routes = Blueprint('well_logs', __name__)
  controller = WellLogController()

  @well_log_routes.route('/well-logs', methods=['GET'])
  def get_all_wells():
    return controller.get_all_wells()


  return well_log_routes