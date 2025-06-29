from unittest import TestCase
from unittest.mock import Mock, patch

import requests.exceptions  # type: ignore

from clients.swapi_client import SWAPIClient

from ..utils.exceptions import SWAPIClientError


class TestSWAPIClient(TestCase):
    def setUp(self) -> None:
        self.client = SWAPIClient(disable_ssl_verification=True)
        self.base_url = "https://swapi.dev/api"

    def _mock_response(self, status: int = 200, content: dict = None, raise_error: bool = False) -> Mock:
        mock_resp = Mock()
        mock_resp.status_code = status
        mock_resp.json.return_value = content or {}
        if raise_error:
            mock_resp.raise_for_status.side_effect = Exception("Mocked error")
        return mock_resp

    @patch("clients.swapi_client.requests.Session.get")
    def test_get_films_success(self, mock_get: Mock) -> None:
        mock_data = {"results": [{"title": "A New Hope", "episode_id": 4, "release_date": "1977-05-25"}]}
        mock_get.return_value = self._mock_response(content=mock_data)

        result = self.client.fetch_films()["results"]

        mock_get.assert_called_once_with(f"{self.base_url}/films/", timeout=10, verify=False)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "A New Hope")

    @patch("clients.swapi_client.requests.Session.get")
    def test_get_characters_success(self, mock_get: Mock) -> None:
        mock_data = {"results": [{"name": "Luke Skywalker", "height": "172", "mass": "77"}]}
        mock_get.return_value = self._mock_response(content=mock_data)

        result = self.client.fetch_people()["results"]

        mock_get.assert_called_once_with(f"{self.base_url}/people/", timeout=10, verify=False)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Luke Skywalker")

    @patch("clients.swapi_client.requests.Session.get")
    def test_get_starships_success(self, mock_get: Mock) -> None:
        mock_data = {
            "results": [
                {
                    "name": "Death Star",
                    "model": "DS-1 Orbital Battle Station",
                    "manufacturer": "Imperial Department of Military Research",
                }
            ]
        }
        mock_get.return_value = self._mock_response(content=mock_data)

        result = self.client.fetch_starships()["results"]

        mock_get.assert_called_once_with(f"{self.base_url}/starships/", timeout=10, verify=False)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Death Star")

    @patch("clients.swapi_client.requests.Session.get")
    def test_get_starships_error(self, mock_get: Mock) -> None:
        http_error = requests.exceptions.HTTPError(response=Mock(status_code=404, reason="Not Found"))
        mock_get.side_effect = http_error

        with self.assertRaises(SWAPIClientError) as exc:
            self.client.fetch_starships()

        self.assertEqual(exc.exception.status_code, 404)
        self.assertEqual(exc.exception.reason, "Not Found")
        self.assertEqual(exc.exception.message, "SWAPI request failed: Not Found")

    @patch("clients.swapi_client.requests.Session.get")
    def test_get_characters_error(self, mock_get: Mock) -> None:
        http_error = requests.exceptions.HTTPError(response=Mock(status_code=503, reason="Service Unavailable"))
        mock_get.side_effect = http_error

        with self.assertRaises(SWAPIClientError) as exc:
            self.client.fetch_people()

        self.assertEqual(exc.exception.status_code, 503)
        self.assertEqual(exc.exception.reason, "Service Unavailable")
        self.assertEqual(exc.exception.message, "SWAPI request failed: Service Unavailable")

    @patch("clients.swapi_client.requests.Session.get")
    def test_get_films_error(self, mock_get: Mock) -> None:
        http_error = requests.exceptions.HTTPError(response=Mock(status_code=500, reason="Unknown Server Error"))
        mock_get.side_effect = http_error

        with self.assertRaises(SWAPIClientError) as exc:
            self.client.fetch_films()

        self.assertEqual(exc.exception.status_code, 500)
        self.assertEqual(exc.exception.reason, "Unknown Server Error")
        self.assertEqual(exc.exception.message, "SWAPI request failed: Unknown Server Error")

    @patch("clients.swapi_client.requests.Session.get")
    def test_get_films_raise_exception(self, mock_get: Mock) -> None:
        mock_get.side_effect = Exception("Unexpected error")

        with self.assertRaises(SWAPIClientError) as exc:
            self.client.fetch_films()

        self.assertEqual(exc.exception.message, "Unexpected error during SWAPI call: Unexpected error")
        self.assertIsNone(exc.exception.status_code)
        self.assertIsNone(exc.exception.reason)
