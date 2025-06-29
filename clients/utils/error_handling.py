from functools import wraps
from typing import Any, Dict

from requests.exceptions import RequestException  # type: ignore

from .exceptions import SWAPIClientError


def swapi_client_error_handler(func):  # type: ignore
    """
    Decorator to handle errors for SWAPIClient methods.
    Catches requests exceptions and raises SWAPIClientError with a descriptive message.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except RequestException as exc:
            raise SWAPIClientError(
                f"SWAPI request failed: {exc.response.reason if exc.response else 'No response received'}",
                status_code=exc.response.status_code if exc.response else None,
                reason=exc.response.reason if exc.response else "No response received",
            ) from exc
        except Exception as exc:
            raise SWAPIClientError(f"Unexpected error during SWAPI call: {exc}") from exc

    return wrapper
