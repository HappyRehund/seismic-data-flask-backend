from dataclasses import dataclass
from typing import Dict, Any, cast
from dto.data.horizon_data import HorizonPointData

@dataclass
class Horizon:
  X: int
  Y: int
  Inline: int
  Crossline: int
  TraceNumber: int
  bottom: float
  bottom_reff: float
  top: float
  top_reff: float

  @classmethod
  def from_dict(cls, data: Dict[str, Any]):
    try:
      return cls(
        X=int(data.get('X', 0)),
        Y=int(data.get('Y', 0)),
        Inline=int(data.get('Inline', 0)),
        Crossline=int(data.get('Crossline', 0)),
        TraceNumber=int(data.get('TraceNumber', 0)),
        bottom=float(data.get('bottom', 0.0)),
        bottom_reff=float(data.get('bottom_reff', 0.0)),
        top=float(data.get('top', 0.0)),
        top_reff=float(data.get('top_reff', 0.0))
      )
    except (ValueError, TypeError) as e:
      raise ValueError(f"Invalid: {str(e)}")

  def to_dict(self) -> HorizonPointData:
    return cast(HorizonPointData, vars(self).copy())