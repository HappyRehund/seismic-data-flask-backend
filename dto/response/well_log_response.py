from dataclasses import dataclass, asdict
from typing import List, cast
from dto.data.well_log_data import WellLogData, WellLogsData

@dataclass
class WellLogResponse:
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

  def to_dict(self) -> WellLogData:
    return cast(WellLogData, asdict(self))

@dataclass
class WellLogsResponse:
  well_logs: List[WellLogResponse]

  @classmethod
  def from_well_log_dicts(cls, well_logs_data: List[WellLogData]):
    well_logs = [WellLogResponse(**data) for data in well_logs_data]
    return cls(well_logs=well_logs)

  def to_dict(self) -> WellLogsData:
    return {
      "well_logs": [log.to_dict() for log in self.well_logs]
    }


