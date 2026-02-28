from typing import Dict, Any, cast
from dataclasses import dataclass, asdict
from dto.data.well_data import WellData

@dataclass
class WellCoordinate:
    inline: int
    crossline: int
    x: float
    y: float
    trace_number: int
    bottom: float
    bottom_reff: float
    top: float
    top_reff: float
    well_x: float
    well_y: float
    well_name: str
    distance: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        try:
            return cls(
                inline=int(data.get('Inline', 0)),
                crossline=int(data.get('Crossline', 0)),
                x=float(data.get('X', 0.0)),
                y=float(data.get('Y', 0.0)),
                trace_number=int(data.get('TraceNumber', 0)),
                bottom=float(data.get('bottom', 0.0)),
                bottom_reff=float(data.get('bottom_reff', 0.0)),
                top=float(data.get('top', 0.0)),
                top_reff=float(data.get('top_reff', 0.0)),
                well_x=cls._parse_coordinate(data.get('Well_X', 0.0)),
                well_y=cls._parse_coordinate(data.get('Well_Y', 0.0)),
                well_name=str(data.get('Well_name', '')),
                distance=float(data.get('distance', 0.0))
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid well coordinate data: {str(e)}")

    @staticmethod
    def _parse_coordinate(value: Any) -> float:
        if isinstance(value, str):
            # Handle format like "407.890.049" -> "407890.049"
            value = value.replace('.', '', value.count('.') - 1) if value.count('.') > 1 else value
        return float(value)

    def to_dict(self) -> WellData:
        return cast(WellData, asdict(self))

    def validate(self) -> bool:
        if not self.well_name:
            raise ValueError("Well name is required")
        if self.inline <= 0 or self.crossline <= 0:
            raise ValueError("Inline and Crossline must be positive")
        return True
