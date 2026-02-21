from flask import Blueprint
from controllers.horizon_controller import HorizonController

def create_well_log_routes() -> Blueprint:
  well_log_routes = Blueprint('horizon', __name__)
  controller = HorizonController()

  @well_log_routes.route('/horizon', methods=['GET'])
  def get_all_wells():
    return controller.get_all_horizons()


  return well_log_routes