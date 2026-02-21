from dataclasses import dataclass
from typing import Dict, Any, cast
from dto.data.well_log_data import WellLogData


def _f(value: Any, default: float = 0.0) -> float:
    """Parse a float, returning default for empty/null/non-numeric values."""
    if value is None or str(value).strip() == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@dataclass
class WellLog:
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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        try:
            return cls(
                id=str(data.get('ID', '')),
                well=str(data.get('WELL', '')),
                depth=_f(data.get('DEPTH')),
                tvdss=_f(data.get('TVDSS')),
                xcoord=_f(data.get('XCOORD')),
                ycoord=_f(data.get('YCOORD')),
                gr=_f(data.get('GR')),
                rt=_f(data.get('RT')),
                rhob=_f(data.get('RHOB')),
                nphi=_f(data.get('NPHI')),
                dt=_f(data.get('DT')),
                dts=_f(data.get('DTS')),
                dtst=_f(data.get('DTST')),
                sp=_f(data.get('SP')),
                phie=_f(data.get('PHIE')),
                phit=_f(data.get('PHIT')),
                vsh=_f(data.get('VSH')),
                swe=_f(data.get('SWE')),
                rwa=_f(data.get('RWA')),
                iqual=_f(data.get('IQUAL')),
                litho=_f(data.get('LITHO')),
                fluid=_f(data.get('FLUID')),
                m=_f(data.get('M')),
                n=_f(data.get('N')),
                zone=_f(data.get('ZONE')),
                marker=_f(data.get('MARKER')),
                fa_status=_f(data.get('FA_STATUS'))
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid well log data: {str(e)}")

    def to_dict(self) -> WellLogData:
        return cast(WellLogData, vars(self).copy())

    def validate(self) -> bool:
        if not self.id or not self.well:
            raise ValueError("ID and Well name are required")
        if self.depth < 0:
            raise ValueError("Depth must be non-negative")
        return True
