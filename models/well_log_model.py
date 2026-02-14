from dataclasses import dataclass
from typing import Dict, Any

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
                well=str(data.get('Well', '')),
                depth=float(data.get('Depth', 0.0)),
                tvdss=float(data.get('TVDSS', 0.0)),
                xcoord=float(data.get('Xcoord', 0.0)),
                ycoord=float(data.get('Ycoord', 0.0)),
                gr=float(data.get('GR', 0.0)),
                rt=float(data.get('RT', 0.0)),
                rhob=float(data.get('RHOB', 0.0)),
                nphi=float(data.get('NPHI', 0.0)),
                dt=float(data.get('DT', 0.0)),
                dts=float(data.get('DTS', 0.0)),
                dtst=float(data.get('DTST', 0.0)),
                sp=float(data.get('SP', 0.0)),
                phie=float(data.get('PHIE', 0.0)),
                phit=float(data.get('PHIT', 0.0)),
                vsh=float(data.get('VSH', 0.0)),
                swe=float(data.get('SWE', 0.0)),
                rwa=float(data.get('RWA', 0.0)),
                iqual=float(data.get('IQUAL', 0.0)),
                litho=float(data.get('LITHO', 0.0)),
                fluid=float(data.get('FLUID', 0.0)),
                m=float(data.get('M', 0.0)),
                n=float(data.get('N', 0.0)),
                zone=float(data.get('ZONE', 0.0)),
                marker=float(data.get('MARKER', 0.0)),
                fa_status=float(data.get('FA_STATUS', 0.0))
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid well log data: {str(e)}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "well": self.well,
            "depth": self.depth,
            "tvdss": self.tvdss,
            "xcoord": self.xcoord,
            "ycoord": self.ycoord,
            "gr": self.gr,
            "rt": self.rt,
            "rhob": self.rhob,
            "nphi": self.nphi,
            "dt": self.dt,
            "dts": self.dts,
            "dtst": self.dtst,
            "sp": self.sp,
            "phie": self.phie,
            "phit": self.phit,
            "vsh": self.vsh,
            "swe": self.swe,
            "rwa": self.rwa,
            "iqual": self.iqual,
            "litho": self.litho,
            "fluid": self.fluid,
            "m": self.m,
            "n": self.n,
            "zone": self.zone,
            "marker": self.marker,
            "fa_status": self.fa_status
        }

    def validate(self) -> bool:
        if not self.id or not self.well:
            raise ValueError("ID and Well name are required")
        if self.depth < 0:
            raise ValueError("Depth must be non-negative")
        return True
