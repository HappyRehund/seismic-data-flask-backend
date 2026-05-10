from typing import Optional, List

from models.image_helper_model import ImageDimensions
from repositories.image_helper_repository import ImageHelperRepository


class ImageHelperService:
    def __init__(self):
        self.repository = ImageHelperRepository()

    def get_image_dimensions(
        self, section_type: str, number: int, dataset: str = 'default'
    ) -> Optional[ImageDimensions]:
        return self.repository.find_image_dimensions(section_type, number, dataset=dataset)

    def get_available_datasets(self) -> List[str]:
        return self.repository.list_datasets()

    def get_section_types(self, dataset: str) -> List[str]:
        return self.repository.list_section_types(dataset)
