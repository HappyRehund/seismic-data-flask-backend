from typing import List, Optional
from repositories.well_log_repository import WellLogRepository, LOG_TYPE_FILES
from models.well_log_model import WellLogData


class WellLogService:
    def __init__(self):
        self.repository = WellLogRepository()

    def _validate_log_type(self, log_type: str) -> str:
        log_type = log_type.lower()
        if log_type not in LOG_TYPE_FILES:
            raise ValueError(f"Invalid log type: '{log_type}'. Valid types: {list(LOG_TYPE_FILES.keys())}")
        return log_type

    def get_all_by_type(self, log_type: str, dataset: str = 'default') -> List[WellLogData]:
        log_type = self._validate_log_type(log_type)
        return self.repository.find_all(log_type, dataset=dataset)

    def get_by_well_name(self, log_type: str, well_name: str, dataset: str = 'default') -> Optional[WellLogData]:
        log_type = self._validate_log_type(log_type)
        if not well_name:
            raise ValueError("Well name is required")
        return self.repository.find_by_well_name(log_type, well_name, dataset=dataset)

    def get_well_names(self, log_type: str, dataset: str = 'default') -> List[str]:
        log_type = self._validate_log_type(log_type)
        return self.repository.get_well_names(log_type, dataset=dataset)

    def get_available_datasets(self) -> List[str]:
        return self.repository.list_datasets()

    def get_log_types(self, dataset: str) -> List[str]:
        return self.repository.list_log_types(dataset)
