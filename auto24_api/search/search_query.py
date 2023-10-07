import datetime as dt
from dataclasses import dataclass
from typing import Union

from auto24_api.abstract_query import AbstractQuery
from auto24_api.search.enums import Make, Sorting, VehiculeType
from auto24_api.search.enums.body_color import BodyColor
from auto24_api.search.enums.drive_type import DriveType
from auto24_api.search.enums.fuel_type import FuelType
from auto24_api.utils.exceptions import QueryParamsValidationError
from auto24_api.utils.query_validators import IsIn, QueryValidator, Validator


@dataclass
class SearchQuery(AbstractQuery):
    vehicule_type: VehiculeType = VehiculeType.CAR
    make: Union[Make, list[Make]] = Make.ALL
    year_from: Union[None, int] = None
    year_to: Union[None, int] = None
    km_from: Union[None, int] = None
    km_to: Union[None, int] = None
    price_from: Union[None, int] = None
    price_to: Union[None, int] = None
    hp_from: Union[None, int] = None
    hp_to: Union[None, int] = None
    drive: DriveType = DriveType.ALL
    fuel_type: Union[FuelType, list[FuelType]] = FuelType.ALL
    body_color: Union[BodyColor, list[BodyColor]] = BodyColor.ALL
    has_warranty: Union[None, bool, str] = None
    is_appraised: Union[None, bool, int] = None
    is_accident_free: Union[None, bool, int] = None
    has_extra_tires: Union[None, bool, int] = None
    sorting: Sorting = Sorting.DEFAULT
    page: Union[None, int] = None
    page_size: Union[None, int] = None

    def __post_init__(self) -> None:
        if isinstance(self.make, Make):
            self.make = [self.make]

        self._qv = QueryValidator(self)
        valid, error = self._qv.validate()
        if not valid:
            raise QueryParamsValidationError(error)
        # Setting the boolean flag to correct value
        if self.has_warranty:
            self.has_warranty = "true"
        if self.is_appraised:
            self.is_appraised = 1
        if self.is_accident_free:
            self.is_accident_free = 2
        if self.has_extra_tires:
            self.has_extra_tires = 1

    @property
    def VALIDATORS(self) -> list[Validator]:
        VALS = [
            IsIn(key="year_from", min=1975, max=dt.datetime.now().year),
            IsIn(key="year_to", min="year_from", max=dt.datetime.now().year),
            IsIn(key="km_from", min=0, max=500_000),
            IsIn(key="km_to", min="km_from", max=500_000),
            IsIn(key="price_from", min=0, max=1_000_000),
            IsIn(key="price_to", min="price_from", max=25_000_000),
            IsIn(key="hp_from", min=0, max=2_500),
            IsIn(key="hp_to", min="hp_from", max=2_500),
            IsIn(key="page", min=1, max=2_500),
            IsIn(key="page_size", min=1, max=60),
        ]
        assert len(self.__annotations__.keys()) == 20, (
            "Validators should be up to date with class input params "
            f"({len(self.__annotations__.keys())})"
        )
        return VALS

    @property
    def KEY_MAPPING(self) -> dict[str, str]:
        MAPPING = {
            "vehicule_type": "vehtyp",
            "make": "make",
            "year_from": "yearfrom",
            "year_to": "yearto",
            "km_from": "kmfrom",
            "km_to": "kmto",
            "price_from": "pricefrom",
            "price_to": "priceto",
            "hp_from": "hpfrom",
            "hp_to": "hpto",
            "drive": "drive",
            "fuel_type": "fuel",
            "body_color": "bodycol",
            "has_warranty": "hw",
            "is_appraised": "prop",
            "is_accident_free": "uprop",
            "has_extra_tires": "extras",
            "sorting": "sort",
            "page": "page",
            "page_size": "pagesize",
        }
        assert len(self.__annotations__.keys()) == len(
            MAPPING.keys()
        ), "Mapping keys should be up to date with class input params"
        return MAPPING
