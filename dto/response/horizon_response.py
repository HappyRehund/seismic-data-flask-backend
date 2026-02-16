from dataclasses import dataclass
from typing import List
from dto.data.horizon_data import HorizonPointData, HorizonData
@dataclass
class HorizonPointResponse:
  X: int
  Y: int
  Inline: int
  Crossline: int
  TraceNumber: int
  bottom: int
  bottom_reff: int
  top: int
  top_reff: int

  def to_dict(self) -> HorizonPointData:
    return {
      "X": self.X,
      "Y": self.Y,
      "Inline": self.Inline,
      "Crossline": self.Crossline,
      "TraceNumber": self.TraceNumber,
      "bottom": self.bottom,
      "bottom_reff": self.bottom_reff,
      "top": self.top,
      "top_reff": self.top_reff
    }

@dataclass
class HorizonResponse:
  horizon: List[HorizonPointResponse]

  @classmethod
  def from_well_log_dicts(cls, horizon_point_data: List[HorizonPointData]):
    horizon = [HorizonPointResponse(**data) for data in horizon_point_data]
    return cls(horizon=horizon)

  def to_dict(self) -> HorizonData:
    return {
      "horizon": [horizon_point.to_dict() for horizon_point in self.horizon]
    }
