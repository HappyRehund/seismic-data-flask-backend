from dataclasses import dataclass
from typing import Dict, Any, Optional, List, cast
from dto.data.well_log_data import WellLogEntryData, WellLogData as WellLogDataDict


@dataclass
class WellLogEntry:
  twt: float
  value: Optional[float]

  @classmethod
  def from_dict(cls, twt: float, raw_value: str) -> 'WellLogEntry':
    value: Optional[float] = None
    if raw_value is not None and raw_value.strip() != '':
      try:
        value = float(raw_value)
      except (ValueError, TypeError):
        value = None
    return cls(twt=twt, value=value)

  def to_dict(self) -> WellLogEntryData:
    return cast(WellLogEntryData, {
      "twt": self.twt,
      "value": self.value
    })


@dataclass
class WellLogData:
  well_name: str
  log_type: str
  entries: List[WellLogEntry]

  def to_dict(self) -> WellLogDataDict:
    return cast(WellLogDataDict, {
      "well_name": self.well_name,
      "log_type": self.log_type,
      "entries": [e.to_dict() for e in self.entries],
      "count": len(self.entries)
    })
