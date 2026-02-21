from typing import List, TypedDict

class HorizonPointData(TypedDict):
  X: int
  Y: int
  Inline: int
  Crossline: int
  TraceNumber: int
  bottom: float
  bottom_reff: float
  top: float
  top_reff: float

class HorizonData(TypedDict):
  horizon: List[HorizonPointData]