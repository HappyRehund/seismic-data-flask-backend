from dataclasses import dataclass, asdict
from typing import List, TypedDict, cast

class WellData(TypedDict):
    """Type definition for well coordinate data dictionary"""
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

class RangeStatisticsData(TypedDict):
    """Type definition for range statistics dictionary"""
    min: int
    max: int
    range: int

class StatisticsData(TypedDict):
    """Type definition for statistics dictionary"""
    inline: RangeStatisticsData
    crossline: RangeStatisticsData

class WellsSummaryData(TypedDict):
    """Type definition for wells summary dictionary"""
    total_wells: int
    statistics: StatisticsData
    well_names: List[str]


class WellsListData(TypedDict):
    """Type definition for wells list dictionary"""
    wells: List[WellData]
    count: int


class WellExistsData(TypedDict):
    """Type definition for well exists response dictionary"""
    exists: bool


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

    def to_dict(self) -> WellData:
        return cast(WellData, asdict(self))

@dataclass
class WellsListResponse:
    """Response DTO for a list of wells"""
    wells: List[WellResponse]
    count: int

    @classmethod
    def from_well_dicts(cls, wells_data: List[WellData]):
        wells = [WellResponse(**data) for data in wells_data]
        return cls(wells=wells, count=len(wells))

    def to_dict(self) -> WellsListData:
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
