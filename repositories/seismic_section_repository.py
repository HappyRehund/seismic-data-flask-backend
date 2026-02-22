import os
from typing import Optional
from models.seismic_section_model import SeismicSection, SectionType


class SeismicSectionRepository:
    def __init__(self, base_path: str = 'csv_data/inline_crossline'):
        self.base_path = base_path

    def _build_path(self, section_type: SectionType, number: int) -> str:
        folder = section_type.value          # 'inline' or 'crossline'
        filename = f"{folder}_{number}.png"
        return os.path.join(self.base_path, folder, filename)

    def find_by_number(
        self, section_type: SectionType, number: int
    ) -> Optional[SeismicSection]:
        path = self._build_path(section_type, number)
        if not os.path.exists(path):
            return None

        with open(path, 'rb') as f:
            image_data = f.read()

        return SeismicSection(
            section_type=section_type,
            section_number=number,
            image_data=image_data,
        )
