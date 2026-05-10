from repositories.horizon_repository import HorizonRepository
from models.horizon_model import Horizon
from typing import List

class HorizonService:
  def __init__(self):
    self.repository = HorizonRepository()

  def get_all_horizons(self, dataset: str = 'horizon') -> List[Horizon]:
    return self.repository.find_all(dataset=dataset)

  def get_all_horizons_page(self, dataset: str = 'horizon', page: int = 1, page_size: int = 500) -> List[Horizon]:
    return self.repository.find_all_page(dataset=dataset, page=page, page_size=page_size)

  def get_available_datasets(self) -> List[str]:
    return self.repository.list_datasets()

  def get_dataset_count(self, dataset: str = 'horizon') -> int:
    return self.repository.count(dataset=dataset)
