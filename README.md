# AutoScout24 Public API

-   [AutoScout24 Public API](#autoscout24-public-api)
    -   [About](#about)
        -   [Disclaimer](#disclaimer)
    -   [Installation](#installation)
    -   [Getting Started](#getting-started)
        -   [Search Listings](#search-listings)
        -   [Listing Details](#listing-details)
        -   [Examples](#examples)

## About

A Public API wrapper written in Python for [www.AutoScout24.ch](https://www.autoscout24.ch/fr) (Swiss car listing website).

This project is still very new, and a lot is missing. (docs, tests, api integrations)

### Disclaimer

This project is a learning experiment and you are fully responsible for its use.

## Installation

```python
pip install git+https://github.com/leonardcser/auto24-api
```

## Getting Started

```python
from auto24_api import Auto24API
```

The `Auto24API()` class initializes a chrome driver instance. The context manager allows to automatically quit the driver. However, if the `Auto24API()` class needs to be called many times, it is recommended to manually create and dispose the driver with `Auto24API().close()`.

### Search Listings

```python
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

```

### Listing Details

```python
from auto24_api.details import DetailsQuery

with Auto24API() as api:
    res = api.listing_details(DetailsQuery(_id=123456, slug="some-car-slug"))

```

### Examples

Check out implementation examples [here](./examples/).
