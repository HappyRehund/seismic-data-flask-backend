from typing import Dict, Any
from dataclasses import dataclass
from dto.well_response import WellData

@dataclass
class WellCoordinate:
    inline: int
    crossline: int
    inline_n: int
    crossline_n: int
    x: float
    y: float
    trace_number: int
    basement: float
    basement_reff: float
    surface: float
    surface_reff: float
    well_x: float
    well_y: float
    well_name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        try:
            return cls(
                inline=int(data.get('Inline', 0)),
                crossline=int(data.get('Crossline', 0)),
                inline_n=int(data.get('Inline_n', 0)),
                crossline_n=int(data.get('Crossline_n', 0)),
                x=float(data.get('X', 0.0)),
                y=float(data.get('Y', 0.0)),
                trace_number=int(data.get('TraceNumber', 0)),
                basement=float(data.get('basement', 0.0)),
                basement_reff=float(data.get('basement_reff', 0.0)),
                surface=float(data.get('surface', 0.0)),
                surface_reff=float(data.get('surface_reff', 0.0)),
                well_x=cls._parse_coordinate(data.get('Well_X', 0.0)),
                well_y=cls._parse_coordinate(data.get('Well_Y', 0.0)),
                well_name=str(data.get('Well_name', ''))
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
        return {
            "inline": self.inline,
            "crossline": self.crossline,
            "inline_n": self.inline_n,
            "crossline_n": self.crossline_n,
            "x": self.x,
            "y": self.y,
            "trace_number": self.trace_number,
            "basement": self.basement,
            "basement_reff": self.basement_reff,
            "surface": self.surface_reff,
            "surface_reff": self.surface_reff,
            "well_x": self.well_x,
            "well_y": self.well_y,
            "well_name": self.well_name
        }

    def validate(self) -> bool:
        if not self.well_name:
            raise ValueError("Well name is required")
        if self.inline <= 0 or self.crossline <= 0:
            raise ValueError("Inline and Crossline must be positive")
        return True
