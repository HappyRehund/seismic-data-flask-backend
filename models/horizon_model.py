from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Horizon:
  X: int
  Y: int
  Inline: int
  Crossline: int
  TraceNumber: int
  bottom: int
  bottom_reff: int
  top: int
  top_reff: int

  @classmethod
  def from_dict(cls, data: Dict[str, Any]):
    try:
      return cls(
        X=int(data.get('X', 0)),
        Y=int(data.get('Y', 0)),
        Inline=int(data.get('Inline', 0)),
        Crossline=int(data.get('Crossline', 0)),
        TraceNumber=int(data.get('TraceNumber', 0)),
        bottom=int(data.get('bottom', 0)),
        bottom_reff=int(data.get('bottom_reff', 0)),
        top=int(data.get('top', 0)),
        top_reff=int(data.get('top_reff', 0))
      )
    except (ValueError, TypeError) as e:
      raise ValueError(f"Invalid: {str(e)}")