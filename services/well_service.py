from typing import List, Optional, Dict, Any
from models.well_model import WellCoordinate
from repositories.well_repository import WellRepository


class WellService:
    def __init__(self):
        """Initialize service with repository dependency"""
        self.repository = WellRepository()

    def get_all_wells(self) -> List[Dict[str, Any]]:
        wells = self.repository.find_all()
        return [well.to_dict() for well in wells]

    def get_well_by_name(self, well_name: str) -> Optional[Dict[str, Any]]:
        if not well_name:
            raise ValueError("Well name is required")

        well = self.repository.find_by_name(well_name)
        return well.to_dict() if well else None

    def get_wells_summary(self) -> Dict[str, Any]:
        wells = self.repository.find_all()

        if not wells:
            return {
                "total_wells": 0,
                "statistics": {}
            }

        inline_values = [w.inline for w in wells]
        crossline_values = [w.crossline for w in wells]

        return {
            "total_wells": len(wells),
            "statistics": {
                "inline": {
                    "min": min(inline_values),
                    "max": max(inline_values),
                    "range": max(inline_values) - min(inline_values)
                },
                "crossline": {
                    "min": min(crossline_values),
                    "max": max(crossline_values),
                    "range": max(crossline_values) - min(crossline_values)
                }
            },
            "well_names": [w.well_name for w in wells]
        }

    def search_wells_by_inline(self, min_inline: int, max_inline: int) -> List[Dict[str, Any]]:
        if min_inline > max_inline:
            raise ValueError("Min inline must be less than or equal to max inline")

        wells = self.repository.find_by_inline_range(min_inline, max_inline)
        return [well.to_dict() for well in wells]

    def search_wells_by_crossline(self, min_crossline: int, max_crossline: int) -> List[Dict[str, Any]]:
        if min_crossline > max_crossline:
            raise ValueError("Min crossline must be less than or equal to max crossline")

        wells = self.repository.find_by_crossline_range(min_crossline, max_crossline)
        return [well.to_dict() for well in wells]

    def get_wells_in_area(
        self,
        min_inline: int,
        max_inline: int,
        min_crossline: int,
        max_crossline: int
    ) -> List[Dict[str, Any]]:
        wells = self.repository.find_all()

        filtered_wells = [
            well for well in wells
            if (min_inline <= well.inline <= max_inline and
                min_crossline <= well.crossline <= max_crossline)
        ]

        return [well.to_dict() for well in filtered_wells]

    def check_well_exists(self, well_name: str) -> bool:
        return self.repository.exists(well_name)
