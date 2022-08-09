# AutoScout24 Public API

- [AutoScout24 Public API](#autoscout24-public-api)
  - [About](#about)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
    - [Search List](#search-list)

## About

This project is still in development and is not ready for use.

## Installation

```python
pip install git+https://github.com/leonardcser/auto24-api
```

## Getting Started

```python
from auto24_api import Auto24API
```

### Search List

```python
from auto24_api.search import Filters, SearchQuery, DetailsQuery

res = Auto24API().search_list(
    SearchQuery(
        vehicule_type=Filters.VEHICULE_TYPE.CAR
        make=[Filters.MAKE.BMW, Filters.MAKE.VW],
        year_from=None,
        year_to=None,
        km_from=None,
        km_to=None,
        price_from=None,
        price_to=None,
        hp_from=None,
        hp_to=None,
        sorting=Filters.SORTING.HP_DESC,
        page=None,
        page_size=None,
    )
```
