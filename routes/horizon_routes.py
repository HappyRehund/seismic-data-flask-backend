from flask import Blueprint
from controllers.horizon_controller import HorizonController

def create_horizon_routes() -> Blueprint:
  horizon_routes = Blueprint('horizon', __name__)
  controller = HorizonController()

  @horizon_routes.route('/horizon-page', methods=['GET'])
  def get_all_horizons_page():
    return controller.get_all_horizons_page()

  @horizon_routes.route('/horizon', methods=['GET'])
  def get_all_horizons():
    return controller.get_all_horizons()

  @horizon_routes.route('/horizon/datasets', methods=['GET'])
  def get_datasets():
    return controller.get_datasets()

  return horizon_routes
