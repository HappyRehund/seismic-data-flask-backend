from typing import TypedDict, List

class WellLogData(TypedDict):
  id: str
  well: str
  depth: float
  tvdss: float
  xcoord: float
  ycoord: float
  gr: float
  rt: float
  rhob: float
  nphi: float
  dt: float
  dts: float
  dtst: float
  sp: float
  phie: float
  phit: float
  vsh: float
  swe: float
  rwa: float
  iqual: float
  litho: float
  fluid: float
  m: float
  n: float
  zone: float
  marker: float
  fa_status: float

class WellLogsData(TypedDict):
  well_logs: List[WellLogData]