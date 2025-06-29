class SWAPIClientError(Exception):
    """Custom error class for SWAPIClient errors."""

    def __init__(self, message: str, status_code: int = None, reason: str = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        status_info = f" (Status: {self.status_code})" if self.status_code else ""
        reason_info = f" (Reason: {self.reason})" if self.reason else ""
        return f"SWAPIClientError: {self.message}{status_info}{reason_info}"
