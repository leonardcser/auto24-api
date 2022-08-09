from dataclasses import dataclass

from auto24_api.utils.abstract_dataclass import AbstractDataclass


@dataclass
class AbstractAuto24APIResponse(AbstractDataclass):
    raw: dict


@dataclass
class Auto24APISearchResponse(AbstractAuto24APIResponse):
    stats: dict
    search_results: dict


@dataclass
class Auto24APIDetailsResponse(AbstractAuto24APIResponse):
    details: dict
