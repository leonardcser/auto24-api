from auto24_api import Auto24API
from auto24_api.details import DetailsQuery


def main() -> None:
    with Auto24API() as api:
        res = api.listing_details(
            DetailsQuery(_id=123456, slug="some-car-slug")
        )
        print(res)


if __name__ == "__main__":
    main()
