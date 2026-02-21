from flask import Blueprint
from controllers.horizon_controller import HorizonController

def create_horizon_routes() -> Blueprint:
  horizon_routes = Blueprint('horizon', __name__)
  controller = HorizonController()

  @horizon_routes.route('/horizon', methods=['GET'])
  def get_all_wells():
    return controller.get_all_horizons()

  return horizon_routes