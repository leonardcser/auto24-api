from dataclasses import dataclass
from typing import Optional


@dataclass
class VehicleSpec:
    first_reg: Optional[str] = None
    body_color: Optional[str] = None
    km: Optional[str] = None
    price: Optional[str] = None
    options: Optional[list[str]] = None
