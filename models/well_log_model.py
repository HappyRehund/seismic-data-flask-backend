from dataclasses import dataclass
from typing import Dict, Any, Optional, List


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

  def to_dict(self) -> dict:
    return {
      "twt": self.twt,
      "value": self.value
    }


@dataclass
class WellLogData:
  well_name: str
  log_type: str
  entries: List[WellLogEntry]

  def to_dict(self) -> dict:
    return {
      "well_name": self.well_name,
      "log_type": self.log_type,
      "entries": [e.to_dict() for e in self.entries],
      "count": len(self.entries)
    }


@dataclass
class WellLogStats:
  """Statistics for a well log type (shared TWT column across all wells)."""
  log_type: str
  total_rows: int
  min_twt: float
  max_twt: float
  max_abs_twt: float
  mid_twt: float

  def to_dict(self) -> dict:
    return {
      "log_type": self.log_type,
      "total_rows": self.total_rows,
      "min_twt": self.min_twt,
      "max_twt": self.max_twt,
      "max_abs_twt": self.max_abs_twt,
      "mid_twt": self.mid_twt
    }


@dataclass
class WellLogWellStats:
  """Statistics for a specific well within a well log type."""
  well_name: str
  log_type: str
  total_rows: int
  min_twt: float
  max_twt: float
  max_abs_twt: float
  mid_twt: float
  non_null_count: int

  def to_dict(self) -> dict:
    return {
      "well_name": self.well_name,
      "log_type": self.log_type,
      "total_rows": self.total_rows,
      "min_twt": self.min_twt,
      "max_twt": self.max_twt,
      "max_abs_twt": self.max_abs_twt,
      "mid_twt": self.mid_twt,
      "non_null_count": self.non_null_count
    }
