import enum


class Sorting(enum.Enum):
    DEFAULT = None
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    KM_ASC = "km_asc"
    KM_DESC = "km_desc"
    YEAR_ASC = "year_asc"
    YEAR_DESC = "year_desc"
    MAKE_MODEL_ASC = "makemodel_asc"
    MAKE_MODEL_DESC = "makemodel_desc"
    HP_DESC = "hp_desc"
