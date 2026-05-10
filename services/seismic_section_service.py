from repositories.seismic_section_repository import SeismicSectionRepository
from models.seismic_section_model import SeismicSection, SectionType
from typing import Optional, List


class SeismicSectionService:
    def __init__(self):
        self.repository = SeismicSectionRepository()

    def get_inline_image(self, number: int, dataset: str = 'default') -> Optional[SeismicSection]:
        return self.repository.find_by_number(SectionType.INLINE, number, dataset=dataset)

    def get_crossline_image(self, number: int, dataset: str = 'default') -> Optional[SeismicSection]:
        return self.repository.find_by_number(SectionType.CROSSLINE, number, dataset=dataset)

    def get_inline_mjb_image(self, number: int, dataset: str = 'default') -> Optional[SeismicSection]:
        return self.repository.find_by_number(SectionType.INLINEMJB, number, dataset=dataset)

    def get_crossline_mjb_image(self, number: int, dataset: str = 'default') -> Optional[SeismicSection]:
        return self.repository.find_by_number(SectionType.CROSSLINEMJB, number, dataset=dataset)

    def get_available_datasets(self) -> List[str]:
        return self.repository.list_datasets()

    def get_section_types(self, dataset: str) -> List[str]:
        return self.repository.list_section_types(dataset)
