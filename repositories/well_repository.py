"""
Repository Layer - Data Access Layer
Handles all CRUD operations with the data source (CSV in this case)
Similar to TypeORM repositories in NestJS
"""
import csv
import os
from typing import List, Optional, Dict, Any
from models.well_model import WellCoordinate


class WellRepository:
    def __init__(self, csv_path: str = 'csv_data/well/well_coordinates.csv'):
        self.csv_path = csv_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

    def find_all(self) -> List[WellCoordinate]:
        wells = []
        try:
            with open(self.csv_path, 'r') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    try:
                        well = WellCoordinate.from_dict(row)
                        wells.append(well)
                    except ValueError as e:
                        # Log error but continue processing
                        print(f"Error parsing row: {e}")
                        continue
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

        return wells

    def find_by_name(self, well_name: str) -> Optional[WellCoordinate]:
        all_wells = self.find_all()
        for well in all_wells:
            if well.well_name == well_name:
                return well
        return None

    def find_by_id(self, well_name: str) -> Optional[WellCoordinate]:
        return self.find_by_name(well_name)

    def find_by_inline_range(self, min_inline: int, max_inline: int) -> List[WellCoordinate]:
        all_wells = self.find_all()
        return [
            well for well in all_wells
            if min_inline <= well.inline <= max_inline
        ]

    def find_by_crossline_range(self, min_crossline: int, max_crossline: int) -> List[WellCoordinate]:
        all_wells = self.find_all()
        return [
            well for well in all_wells
            if min_crossline <= well.crossline <= max_crossline
        ]

    def count(self) -> int:
        return len(self.find_all())

    def exists(self, well_name: str) -> bool:
        return self.find_by_name(well_name) is not None