import os
from typing import Optional
from models.seismic_section_model import SeismicSection, SectionType


class SeismicSectionRepository:
    def __init__(self, base_path: str = 'csv_data/inline_crossline'):
        self.base_path = base_path

    def _build_candidate_paths(self, section_type: SectionType, number: int) -> list[str]:
        if section_type == SectionType.INLINE:
            return [
                os.path.join(self.base_path, 'inline', f'inline_{number}.png'),
            ]

        if section_type == SectionType.CROSSLINE:
            return [
                os.path.join(self.base_path, 'crossline', f'crossline_{number}.png'),
            ]

        if section_type == SectionType.INLINEMJB:
            return [
                os.path.join(self.base_path, 'inlineMJB', f'inline_{number}.png'),
                os.path.join(self.base_path, 'inlineMJB', f'inlineMJB_{number}.png'),
            ]

        if section_type == SectionType.CROSSLINEMJB:
            return [
                os.path.join(
                    self.base_path,
                    'crosslineMJB',
                    'crosslineMJB',
                    f'crossline_{number}.png',
                ),
                os.path.join(self.base_path, 'crosslineMJB', f'crossline_{number}.png'),
                os.path.join(
                    self.base_path,
                    'crosslineMJB',
                    f'crosslineMJB_{number}.png',
                ),
            ]

        return []

    def find_by_number(
        self, section_type: SectionType, number: int
    ) -> Optional[SeismicSection]:
        path = next(
            (candidate for candidate in self._build_candidate_paths(section_type, number)
             if os.path.exists(candidate)),
            None,
        )
        if path is None:
            return None

        with open(path, 'rb') as f:
            image_data = f.read()

        return SeismicSection(
            section_type=section_type,
            section_number=number,
            image_data=image_data,
        )
