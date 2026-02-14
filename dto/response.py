from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class WellResponse:
    """Response DTO for a single well coordinate"""
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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class WellsListResponse:
    """Response DTO for a list of wells"""
    wells: List[WellResponse]
    count: int

    @classmethod
    def from_well_dicts(cls, wells_data: List[Dict[str, Any]]) -> 'WellsListResponse':
        wells = [WellResponse(**data) for data in wells_data]
        return cls(wells=wells, count=len(wells))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wells": [well.to_dict() for well in self.wells],
            "count": self.count
        }


@dataclass
class RangeStatistics:
    """Statistics for inline or crossline range"""
    min: int
    max: int
    range: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StatisticsResponse:
    """Statistics response containing inline and crossline stats"""
    inline: RangeStatistics
    crossline: RangeStatistics

    def to_dict(self) -> Dict[str, Any]:
        return {
            "inline": self.inline.to_dict(),
            "crossline": self.crossline.to_dict()
        }


@dataclass
class WellsSummaryResponse:
    """Response DTO for wells summary"""
    total_wells: int
    statistics: StatisticsResponse
    well_names: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WellsSummaryResponse':
        stats_data = data.get('statistics', {})
        inline_stats = RangeStatistics(**stats_data.get('inline', {}))
        crossline_stats = RangeStatistics(**stats_data.get('crossline', {}))
        statistics = StatisticsResponse(inline=inline_stats, crossline=crossline_stats)

        return cls(
            total_wells=data.get('total_wells', 0),
            statistics=statistics,
            well_names=data.get('well_names', [])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_wells": self.total_wells,
            "statistics": self.statistics.to_dict(),
            "well_names": self.well_names
        }


@dataclass
class WellExistsResponse:
    """Response DTO for well existence check"""
    exists: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
