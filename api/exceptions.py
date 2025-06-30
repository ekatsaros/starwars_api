"""
Custom exceptions for the Star Wars API.
"""

import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import DatabaseError
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


class StarWarsAPIException(Exception):
    """Base exception for Star Wars API specific errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UniqueConstraintError(IntegrityError):
    """Exception raised when a unique constraint is violated."""

    pass


class DatabaseOperationError(StarWarsAPIException):
    """Exception raised when database operations fail."""

    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResourceNotFoundError(StarWarsAPIException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource_type: str, identifier: str):
        message = f"{resource_type} with identifier '{identifier}' not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class InvalidSearchTermError(StarWarsAPIException):
    """Exception raised when search term is invalid."""

    def __init__(self, message: str = "Invalid search term provided"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


def custom_exception_handler(exc: Exception, context: dict) -> Response:
    """
    Custom exception handler for the Star Wars API.
    Handles both DRF exceptions and custom exceptions.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Handle custom Star Wars API exceptions
    if isinstance(exc, StarWarsAPIException):
        custom_response_data = {
            "error": exc.message,
            "status_code": exc.status_code,
            "timestamp": context["request"].META.get("REQUEST_TIME", None),
        }

        logger.error(f"StarWarsAPIException: {exc.message}", exc_info=True)
        return Response(custom_response_data, status=exc.status_code)

    # Handle database errors
    elif isinstance(exc, DatabaseError):
        custom_response_data = {
            "error": "A database error occurred. Please try again later.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "timestamp": context["request"].META.get("REQUEST_TIME", None),
        }

        logger.error(f"Database error: {str(exc)}", exc_info=True)
        return Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Handle Django validation errors
    elif isinstance(exc, DjangoValidationError):
        custom_response_data = {
            "error": "Validation error occurred",
            "details": exc.message_dict if hasattr(exc, "message_dict") else str(exc),
            "status_code": status.HTTP_400_BAD_REQUEST,
            "timestamp": context["request"].META.get("REQUEST_TIME", None),
        }

        logger.warning(f"Validation error: {str(exc)}")
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

    # If we have a DRF response, enhance it with additional context
    if response is not None:
        custom_response_data = {
            "error": response.data,
            "status_code": response.status_code,
            "timestamp": context["request"].META.get("REQUEST_TIME", None),
        }
        response.data = custom_response_data

        logger.warning(f"DRF exception: {response.data}", exc_info=True)

    return response
