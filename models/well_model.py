from typing import Dict, Any, List
from dataclasses import dataclass, asdict

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

    def to_dict(self) -> dict:
        return asdict(self)

    def validate(self) -> bool:
        if not self.well_name:
            raise ValueError("Well name is required")
        if self.inline <= 0 or self.crossline <= 0:
            raise ValueError("Inline and Crossline must be positive")
        return True


@dataclass
class RangeStatistics:
    """Statistics for inline or crossline range"""
    min: int
    max: int
    range: int

    def to_dict(self) -> dict:
        return {
            "min": self.min,
            "max": self.max,
            "range": self.range
        }


@dataclass
class StatisticsResponse:
    """Statistics response containing inline and crossline stats"""
    inline: RangeStatistics
    crossline: RangeStatistics

    def to_dict(self) -> dict:
        return {
            "inline": self.inline.to_dict(),
            "crossline": self.crossline.to_dict()
        }


@dataclass
class WellsSummaryResponse:
    """Response for wells summary"""
    total_wells: int
    statistics: StatisticsResponse
    well_names: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'WellsSummaryResponse':
        stats_data = data.get('statistics', {})
        inline_stats = RangeStatistics(**stats_data.get('inline', {}))
        crossline_stats = RangeStatistics(**stats_data.get('crossline', {}))
        statistics = StatisticsResponse(inline=inline_stats, crossline=crossline_stats)

        return cls(
            total_wells=data.get('total_wells', 0),
            statistics=statistics,
            well_names=data.get('well_names', [])
        )

    def to_dict(self) -> dict:
        return {
            "total_wells": self.total_wells,
            "statistics": self.statistics.to_dict(),
            "well_names": self.well_names
        }


@dataclass
class WellExistsResponse:
    """Response for well existence check"""
    exists: bool

    def to_dict(self) -> dict:
        return {
            "exists": self.exists
        }
