from abc import ABC, abstractmethod

from auto24_api.utils.query_validators import Validator


class AbstractQuery(ABC):
    @property
    @abstractmethod
    def VALIDATORS(self) -> list[Validator]:
        pass

    @property
    @abstractmethod
    def KEY_MAPPING(self) -> dict[str, str]:
        pass
