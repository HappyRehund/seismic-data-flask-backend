from typing import List, Optional, TypedDict


class WellLogEntryData(TypedDict):
  twt: float
  value: Optional[float]


class WellLogData(TypedDict):
  well_name: str
  log_type: str
  entries: List[WellLogEntryData]
  count: int
