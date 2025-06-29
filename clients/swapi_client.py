import os
from typing import Any

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
    def fetch_resource(self, resource: str, page: int = 1) -> dict:
        """Fetch a specific resource from SWAPI, paginated by page number."""
        url = f"{self.BASE_URL}/{resource}/?page={page}"
        resp = self.session.get(url, timeout=10, verify=not self.disable_ssl_verification)
        resp.raise_for_status()
        return resp.json()

    def fetch_all(self, resource: str) -> list[Any]:
        """Fetch all items for a SWAPI resource (all pages)."""
        results = []
        page = 1
        while True:
            data = self.fetch_resource(resource, page=page)
            results.extend(data.get("results", []))
            if not data.get("next"):
                break
            page += 1
        return results

    def fetch_people(self) -> list[Any]:
        return self.fetch_all("people")

    def fetch_films(self) -> list[Any]:
        return self.fetch_all("films")

    def fetch_starships(self) -> list[Any]:
        return self.fetch_all("starships")
