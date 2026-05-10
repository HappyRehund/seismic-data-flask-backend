from typing import List, Optional
from repositories.well_repository import WellRepository
from models.well_model import WellCoordinate

class WellService:
    def __init__(self):
        self.repository = WellRepository()

    def get_all_wells(self, dataset: str = 'well_coordinatesmj_B_G') -> List[WellCoordinate]:
        return self.repository.find_all(dataset=dataset)

    def get_well_by_name(self, well_name: str, dataset: str = 'well_coordinatesmj_B_G') -> Optional[WellCoordinate]:
        if not well_name:
            raise ValueError("Well name is required")
        return self.repository.find_by_name(well_name, dataset=dataset)

    def get_wells_summary(self, dataset: str = 'well_coordinatesmj_B_G') -> dict:
        wells = self.repository.find_all(dataset=dataset)

        if not wells:
            return {
                "total_wells": 0,
                "statistics": {
                    "inline": {"min": 0, "max": 0, "range": 0},
                    "crossline": {"min": 0, "max": 0, "range": 0}
                },
                "well_names": []
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

    def check_well_exists(self, well_name: str, dataset: str = 'well_coordinatesmj_B_G') -> bool:
        return self.repository.exists(well_name, dataset=dataset)

    def get_available_datasets(self) -> List[str]:
        return self.repository.list_datasets()
