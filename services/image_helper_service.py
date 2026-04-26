from typing import Optional

from models.image_helper_model import ImageDimensions
from repositories.image_helper_repository import ImageHelperRepository


class ImageHelperService:
    def __init__(self):
        self.repository = ImageHelperRepository()

    def get_image_dimensions(
        self, section_type: str, number: int
    ) -> Optional[ImageDimensions]:
        return self.repository.find_image_dimensions(section_type, number)