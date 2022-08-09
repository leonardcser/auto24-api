from auto24_api import Auto24API
from auto24_api.search import Filters, SearchQuery

with Auto24API() as api:
    res = api.search_listings(
        SearchQuery(
            make=[Filters.MAKE.AUDI, Filters.MAKE.BMW, Filters.MAKE.VW],
            year_from=2014,
            year_to=None,
            km_from=None,
            km_to=60_000,
            price_from=7_500,
            price_to=20_000,
            hp_from=180,
            sorting=Filters.SORTING.HP_DESC,
            page_size=60,
        )
    )
