import logging
from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base exception for all application-level errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "INTERNAL_SERVER_ERROR"
    message: str = "An internal application error occurred."

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message or self.message)
        if message:
            self.message = message
        if code:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        """Format error payload in consistent canonical JSON shape."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "NOT_FOUND"
    message = "The requested resource was not found."


class AuthorizationError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "AUTHORIZATION_ERROR"
    message = "Access denied."


class AuthenticationError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTHENTICATION_ERROR"
    message = "Authentication required."


class ValidationError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT if hasattr(status, "HTTP_422_UNPROCESSABLE_CONTENT") else 422
    code = "VALIDATION_ERROR"
    message = "Validation failed for the requested operation."



class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "CONFLICT_ERROR"
    message = "A resource conflict was detected."


class RateLimitedError(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "RATE_LIMITED"
    message = "Rate limit exceeded. Please try again later."


class UpstreamIntegrationError(AppError):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "UPSTREAM_INTEGRATION_ERROR"
    message = "An upstream integration service error occurred."


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """FastAPI exception handler for typed AppError exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """FastAPI exception handler catching all unhandled exceptions safely without leaking internal details."""
    logger.error("Unhandled server exception on %s %s: %s", request.method, request.url, str(exc), exc_info=True)
    error_payload = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please contact support.",
            "details": None,
        }
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_payload,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Register application exception handlers on FastAPI instance."""
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
