from dataclasses import dataclass

from auto24_api.abstract_query import AbstractQuery
from auto24_api.utils.query_validators import Validator


@dataclass
class DetailsQuery(AbstractQuery):
    _id: int
    slug: str

    @property
    def VALIDATORS(self) -> list[Validator]:
        return []

    @property
    def KEY_MAPPING(self) -> dict[str, str]:
        assert (
            len(self.__annotations__.keys()) == 2
        ), "Mapping keys should be up to date with class input params"
        return {
            "_id": "vehid",
        }
