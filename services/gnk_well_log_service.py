from typing import List, Optional
from repositories.gnk_well_log_repository import GnkWellLogRepository
from models.gnk_well_log_model import GnkWellLogEntry


class GnkWellLogService:
    def __init__(self):
        self.repository = GnkWellLogRepository()

    def get_all(self) -> List[GnkWellLogEntry]:
        return self.repository.find_all()

    def get_by_well(self, well_name: str) -> List[GnkWellLogEntry]:
        if not well_name:
            raise ValueError("Well name is required")
        return self.repository.find_by_well(well_name)

    def get_well_names(self) -> List[str]:
        return self.repository.get_well_names()

    def count(self) -> int:
        return self.repository.count()
