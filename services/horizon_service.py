from repositories.horizon_repository import HorizonRepository
from models.horizon_model import Horizon
from typing import List

class HorizonService:
  def __init__(self):
    self.repository = HorizonRepository()

  def get_all_horizons(self, page: int = 1, page_size: int = 500) -> List[Horizon]:
    return self.repository.find_all(page=page, page_size=page_size)