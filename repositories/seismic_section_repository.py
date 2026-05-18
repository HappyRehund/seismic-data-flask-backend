import os
import re
from typing import Optional, List, Dict

from models.seismic_section_model import SeismicSection, SectionType, SectionRange
from repositories.base_seismic_repository import BaseSeismicRepository


class SeismicSectionRepository(BaseSeismicRepository):
    def _build_candidate_paths(self, section_type: SectionType, dataset: str, number: int) -> list[str]:
        base = self._get_base_path(dataset)

        if section_type == SectionType.INLINE:
            return [
                os.path.join(base, 'inline', f'inline_{number}.png'),
            ]

        if section_type == SectionType.CROSSLINE:
            return [
                os.path.join(base, 'crossline', f'crossline_{number}.png'),
            ]

        return []

    def find_by_number(
        self, section_type: SectionType, number: int, dataset: str = 'default'
    ) -> Optional[SeismicSection]:
        path = next(
            (candidate for candidate in self._build_candidate_paths(section_type, dataset, number)
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

    def get_section_ranges(self, dataset: str = 'default') -> Dict[str, Optional[SectionRange]]:
        """Scan the dataset directories and return min/max/count for each section type."""
        base = self._get_base_path(dataset)
        ranges: Dict[str, Optional[SectionRange]] = {}

        for section_type in SectionType:
            section_dir = os.path.join(base, section_type.value)
            if not os.path.isdir(section_dir):
                continue

            numbers: List[int] = []
            pattern = re.compile(rf"^{section_type.value}_(\d+)\.png$")

            for filename in os.listdir(section_dir):
                match = pattern.match(filename)
                if match:
                    numbers.append(int(match.group(1)))

            if numbers:
                ranges[section_type.value] = SectionRange(
                    min=min(numbers),
                    max=max(numbers),
                    count=len(numbers),
                )

        return ranges
