from auto24_api import Auto24API
from auto24_api.details import DetailsQuery

res = Auto24API().listing_details(
    DetailsQuery(_id=123456, slug="some-car-slug")
)
