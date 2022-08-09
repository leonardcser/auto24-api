import json
import os
import random
import time
from typing import Union

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from auto24_api.details import DetailsQuery
from auto24_api.responses import (
    Auto24APIDetailsResponse,
    Auto24APISearchResponse,
)
from auto24_api.search import SearchQuery
from auto24_api.utils.exceptions import (
    DataNotFoundException,
    InvalidArgsException,
    ReCaptchaRequiredException,
)
from auto24_api.utils.query_encoder_factory import QueryEncoderFactory


class Auto24API:
    def __init__(
        self,
        use_session=True,
        # bypass_captcha=False,
        # proxies=None,
        wait_range=(2, 5),
        max_retries=3,
        lang="fr",
        tmp_dir=".",
    ):
        """
        Args:
            use_session (bool, optional): Whether to use Python Requests
                session in order to keep cookies. When True, the session is
                saved to ".autoapi/tmp/". Defaults to True.
            #bypass_captcha (bool, optional): Automatically tries to complete
                the reCAPTCHA. Defaults to False.
            #proxies (_type_, optional): Python Requests proxies. Defaults to
                None.
            wait_range (tuple, optional): A random wait time in seconds
                between the provided interval will be used between requests.
                Defaults to (2, 5).
            max_retries (int, optional): The number of retries if it failed to
                fetch the data. Defaults to 3.
            lang (str, optional): The translated version of the AutoScout24
                language ("fr", "de" or "it"). Defaults to "fr".
            tmp_dir (str, optional): The directory where to save the temporary
                files (".auto24api"). Defaults to ".".

        Raises:
            InvalidLanguageException: _description_
        """
        self._use_session = use_session
        if lang not in ["fr", "de", "it"]:
            raise InvalidArgsException(
                (
                    "The provided 'lang' is invalid. Choose from "
                    "'fr', 'de' and 'it'."
                )
            )
        else:
            self._lang = lang
        if len(wait_range) != 2 or wait_range[0] > wait_range[1]:
            raise InvalidArgsException(
                (
                    "The provided 'wait_range' is invalid. Length must be "
                    "equal to 2 and first element must be greater than the "
                    "second."
                )
            )
        self._wait_range = wait_range
        self._max_retries = max_retries
        self._tmp_dir = tmp_dir
        self._driver = self._configure_driver()

    def _configure_driver(self) -> uc.Chrome:
        caps = DesiredCapabilities.CHROME
        caps["goog:loggingPrefs"] = {"performance": "ALL"}
        options = uc.ChromeOptions()
        options.headless = True
        user_data_dir = (
            os.path.join(self._tmp_dir, ".auto24api", "driver-user-data")
            if self._use_session
            else None
        )
        return uc.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            user_data_dir=user_data_dir,
            options=options,
            desired_capabilities=caps,
        )

    @property
    def _LIST_URL(self) -> str:
        LANG_MAP = {
            "fr": "fr/voitures",
            "de": "de/autos",
            "it": "it/automobili",
        }
        return f"https://www.autoscout24.ch/{LANG_MAP[self._lang]}/s"

    @property
    def _DETAILS_URL(self) -> str:
        return f"https://www.autoscout24.ch/{self._lang}/d/"

    @property
    def _SESSION_FILENAME(self) -> str:
        return "session.pkl"

    def _get_full_url(self, base_url, query_params: str) -> requests.Response:
        return f"{base_url}?{query_params}"

    def search_listings(self, query: SearchQuery) -> Auto24APISearchResponse:
        full_url = self._get_full_url(
            self._LIST_URL, QueryEncoderFactory(query).data
        )
        data = self._extract_data(full_url)
        return Auto24APISearchResponse(
            raw=data,
            stats=data["search"]["stats"],
            search_results=data["searchResults"],
        )

    def listing_details(self, query: DetailsQuery) -> Auto24APIDetailsResponse:
        full_url = self._get_full_url(
            self._DETAILS_URL + query.slug, QueryEncoderFactory(query).data
        )
        data = self._extract_data(full_url)
        return Auto24APIDetailsResponse(
            raw=data,
            details=data["details"],
        )

    def _extract_data(self, url: str) -> Union[dict, None]:
        tries = 0
        while tries < self._max_retries:
            print(url)
            self._driver.get(url)
            body = self._parse_network(url)
            soup = BeautifulSoup(body, "html.parser")
            # Check if recaptcha is required
            if soup.find("div", attrs={"id": "captcha"}) or soup.find(
                "title", string="Anti-Bot Captcha"
            ):
                raise ReCaptchaRequiredException()
            # Extract data
            script_tag = soup.find("script", attrs={"id": "initial-state"})
            if not script_tag:
                tries += 1
                time.sleep(random.uniform(*self._wait_range))
                continue
            return json.loads(self._parsejs_to_json(script_tag.text))
        raise DataNotFoundException()

    def _parse_network(self, url: str) -> Union[str, None]:
        logs = self._driver.get_log("performance")
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
            ):
                body = self._parse_log(log, url)
                if body and body.startswith("<!DOCTYPE html>"):
                    return body
        return None

    def _parse_log(self, log: dict, url: str) -> Union[str, None]:
        if (
            "params" in log
            and "type" in log["params"]
            and log["params"]["type"] == "Document"
            and "documentURL" in log["params"]
            and log["params"]["documentURL"] == url
        ):
            try:
                return self._driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": log["params"]["requestId"]},
                )["body"]
            except (exceptions.WebDriverException, KeyError):
                return None

    def _parsejs_to_json(self, js: str) -> str:
        js = js.replace("window.INITIAL_STATE = ", "")
        js = js.replace("undefined", "null")
        js = js.replace("};", "}")
        return js
