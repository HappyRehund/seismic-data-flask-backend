from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class GnkWellLogEntry:
    id: str
    well: str
    depth: float
    tvdss: float
    xcoord: float
    ycoord: float
    gr: Optional[float]
    rt: Optional[float]
    rhob: Optional[float]
    nphi: Optional[float]
    dt: Optional[float]
    dts: Optional[float]
    dtst: Optional[float]
    sp: Optional[float]
    phie: Optional[float]
    phit: Optional[float]
    vsh: Optional[float]
    swe: Optional[float]
    swt: Optional[float]
    rwa: Optional[float]
    iqual: Optional[str]
    litho: Optional[str]
    fluid: Optional[str]
    m: Optional[float]
    n: Optional[float]
    zone: Optional[str]
    marker: Optional[str]
    fa_status: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GnkWellLogEntry':
        def parse_float(value: Any, default: Optional[float] = None) -> Optional[float]:
            if value is None or str(value).strip() == '' or str(value).strip() == '-999.25':
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default

        def parse_str(value: Any) -> Optional[str]:
            if value is None or str(value).strip() == '' or str(value).strip() == '-999.25':
                return None
            return str(value).strip()

        return cls(
            id=str(data.get('ID', '')).strip(),
            well=str(data.get('WELL', '')).strip(),
            depth=parse_float(data.get('DEPTH', 0.0), 0.0),
            tvdss=parse_float(data.get('TVDSS', 0.0), 0.0),
            xcoord=parse_float(data.get('XCOORD', 0.0), 0.0),
            ycoord=parse_float(data.get('YCOORD', 0.0), 0.0),
            gr=parse_float(data.get('GR')),
            rt=parse_float(data.get('RT')),
            rhob=parse_float(data.get('RHOB')),
            nphi=parse_float(data.get('NPHI')),
            dt=parse_float(data.get('DT')),
            dts=parse_float(data.get('DTS')),
            dtst=parse_float(data.get('DTST')),
            sp=parse_float(data.get('SP')),
            phie=parse_float(data.get('PHIE')),
            phit=parse_float(data.get('PHIT')),
            vsh=parse_float(data.get('VSH')),
            swe=parse_float(data.get('SWE')),
            swt=parse_float(data.get('SWT')),
            rwa=parse_float(data.get('RWA')),
            iqual=parse_str(data.get('IQUAL')),
            litho=parse_str(data.get('LITHO')),
            fluid=parse_str(data.get('FLUID')),
            m=parse_float(data.get('M')),
            n=parse_float(data.get('N')),
            zone=parse_str(data.get('ZONE')),
            marker=parse_str(data.get('MARKER')),
            fa_status=parse_str(data.get('FA_STATUS')),
        )

    def to_dict(self) -> dict:
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
            "swt": self.swt,
            "rwa": self.rwa,
            "iqual": self.iqual,
            "litho": self.litho,
            "fluid": self.fluid,
            "m": self.m,
            "n": self.n,
            "zone": self.zone,
            "marker": self.marker,
            "fa_status": self.fa_status,
        }
