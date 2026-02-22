from repositories.seismic_section_repository import SeismicSectionRepository
from models.seismic_section_model import SeismicSection, SectionType
from typing import Optional


class SeismicSectionService:
    def __init__(self):
        self.repository = SeismicSectionRepository()

    def get_inline_image(self, number: int) -> Optional[SeismicSection]:
        return self.repository.find_by_number(SectionType.INLINE, number)

    def get_crossline_image(self, number: int) -> Optional[SeismicSection]:
        return self.repository.find_by_number(SectionType.CROSSLINE, number)
