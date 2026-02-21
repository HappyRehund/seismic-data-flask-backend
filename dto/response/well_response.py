from dataclasses import dataclass
from typing import List
from dto.data.well_data import RangeStatisticsData, StatisticsData, WellExistsData, WellsSummaryData

@dataclass
class RangeStatistics:
    """Statistics for inline or crossline range"""
    min: int
    max: int
    range: int

    def to_dict(self) -> RangeStatisticsData:
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

    def to_dict(self) -> StatisticsData:
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
    def from_dict(cls, data: WellsSummaryData) -> 'WellsSummaryResponse':
        stats_data = data.get('statistics', {})
        inline_stats = RangeStatistics(**stats_data.get('inline', {}))
        crossline_stats = RangeStatistics(**stats_data.get('crossline', {}))
        statistics = StatisticsResponse(inline=inline_stats, crossline=crossline_stats)

        return cls(
            total_wells=data.get('total_wells', 0),
            statistics=statistics,
            well_names=data.get('well_names', [])
        )

    def to_dict(self) -> WellsSummaryData:
        return {
            "total_wells": self.total_wells,
            "statistics": self.statistics.to_dict(),
            "well_names": self.well_names
        }


@dataclass
class WellExistsResponse:
    """Response DTO for well existence check"""
    exists: bool

    def to_dict(self) -> WellExistsData:
        return {
            "exists": self.exists
        }
