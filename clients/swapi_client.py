import os

import requests  # type: ignore

from clients.utils.error_handling import swapi_client_error_handler


class SWAPIClient:
    """
    A client for interacting with the Star Wars API (SWAPI).
    """

    BASE_URL = os.environ.get("SWAPI_BASE_URL", "https://swapi.dev/api")

    def __init__(self, session: requests.Session = None, disable_ssl_verification: bool = False) -> None:
        self.session = session or requests.Session()
        self.disable_ssl_verification = disable_ssl_verification

    @swapi_client_error_handler
    def fetch_all(self, resource: str) -> dict:
        url = f"{self.BASE_URL}/{resource}/"
        resp = self.session.get(url, timeout=10, verify=not self.disable_ssl_verification)
        resp.raise_for_status()
        return resp.json()

    def fetch_people(self) -> dict:
        return self.fetch_all("people")

    def fetch_films(self) -> dict:
        return self.fetch_all("films")

    def fetch_starships(self) -> dict:
        return self.fetch_all("starships")
