from typing import TypedDict, List

class WellData(TypedDict):
    """Type definition for well coordinate data dictionary"""
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


