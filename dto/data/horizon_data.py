from typing import List, TypedDict

class HorizonPointData(TypedDict):
  X: int
  Y: int
  Inline: int
  Crossline: int
  TraceNumber: int
  bottom: int
  bottom_reff: int
  top: int
  top_reff: int

class HorizonData(TypedDict):
  horizon: List[HorizonPointData]