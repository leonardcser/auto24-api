from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlencode

from auto24_api.abstract_query import AbstractQuery


@dataclass
class QueryEncoderFactory:
    cls: AbstractQuery

    def __post_init__(self) -> None:
        data = {}
        for k, k_map in self.cls.KEY_MAPPING.items():
            cls_value = getattr(self.cls, k)
            # This function call is placed before the check because some enum
            # entries are None (for the default)
            cls_value = self._convert_to_enum_values(cls_value)
            if cls_value is not None:
                cls_value = self._convert_list_to_str(cls_value)
                data[k_map] = cls_value
        self.data = urlencode(data)

    def _convert_to_enum_values(self, cls_value):
        if isinstance(cls_value, Enum):
            return cls_value.value
        if isinstance(cls_value, list):
            return [c.value for c in cls_value if isinstance(c, Enum)]
        return cls_value

    def _convert_list_to_str(self, cls_value):
        if isinstance(cls_value, list):
            cls_value = ",".join(map(str, cls_value))
        return cls_value
