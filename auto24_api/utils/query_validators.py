from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from auto24_api.utils.abstract_dataclass import AbstractDataclass

if TYPE_CHECKING:
    from auto24_api.abstract_query import AbstractQuery


@dataclass
class Validator(AbstractDataclass):
    key: str

    def __post_init__(self):
        self.error = ""

    @abstractmethod
    def validate(self, cls: object, value: Union[None, int]) -> bool:
        pass


@dataclass
class IsIn(Validator):
    min: Union[int, str]
    max: Union[int, str]

    def validate(self, cls: object, value: Union[None, int]) -> bool:
        if value is None:
            return True

        min_repr = ""
        if isinstance(self.min, str):
            min_repr = f"{self.min}="
            self.min = getattr(cls, self.min) or 0

        max_repr = ""
        if isinstance(self.max, str):
            max_repr = f"{self.max}="
            self.max = getattr(cls, self.max) or 0

        if isinstance(value, int):
            if not self.min <= value <= self.max:
                self.error = (
                    f"'{self.key}' is out of range "
                    f"({min_repr}{self.min} <= "
                    f"{self.key}={value} <= "
                    f"{max_repr}{self.max})"
                )
                return False
            return True


@dataclass
class QueryValidator:
    cls: "AbstractQuery"

    def validate(self) -> tuple[bool, Union[str, None]]:
        for v in self.cls.VALIDATORS:
            value = getattr(self.cls, v.key)
            if not v.validate(self.cls, value):
                return False, v.error
        return True, None
