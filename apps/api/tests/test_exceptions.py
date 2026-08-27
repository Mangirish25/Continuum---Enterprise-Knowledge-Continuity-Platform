import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.api.app.core.exceptions import (
    AppError,
    NotFoundError,
    AuthorizationError,
    AuthenticationError,
    ValidationError,
    ConflictError,
    RateLimitedError,
    UpstreamIntegrationError,
    setup_exception_handlers,
)


def test_exception_hierarchy_attributes():
    """Verify each exception type has correct default status code, code string, and formatting."""
    err_not_found = NotFoundError()
    assert err_not_found.status_code == 404
    assert err_not_found.code == "NOT_FOUND"
    assert err_not_found.to_dict() == {
        "error": {
            "code": "NOT_FOUND",
            "message": "The requested resource was not found.",
            "details": None,
        }
    }

    err_authz = AuthorizationError("Custom access denied message")
    assert err_authz.status_code == 403
    assert err_authz.code == "AUTHORIZATION_ERROR"
    assert err_authz.message == "Custom access denied message"

    err_authn = AuthenticationError()
    assert err_authn.status_code == 401
    assert err_authn.code == "AUTHENTICATION_ERROR"

    err_val = ValidationError(details=[{"field": "email", "issue": "invalid"}])
    assert err_val.status_code == 422
    assert err_val.code == "VALIDATION_ERROR"
    assert err_val.details == [{"field": "email", "issue": "invalid"}]

    err_conflict = ConflictError()
    assert err_conflict.status_code == 409
    assert err_conflict.code == "CONFLICT_ERROR"

    err_rate = RateLimitedError()
    assert err_rate.status_code == 429
    assert err_rate.code == "RATE_LIMITED"

    err_upstream = UpstreamIntegrationError("GitHub API rate limit exceeded")
    assert err_upstream.status_code == 502
    assert err_upstream.code == "UPSTREAM_INTEGRATION_ERROR"


def test_gemini_limit_error_subclass_compatibility():
    """Verify GeminiLimitError (Phase 8) can seamlessly subclass RateLimitedError."""
    class DummyGeminiLimitError(RateLimitedError):
        code = "GEMINI_RATE_LIMITED"
        message = "Gemini API rate limit exceeded."

    gemini_err = DummyGeminiLimitError(details={"rpm_limit": 60})
    assert isinstance(gemini_err, RateLimitedError)
    assert isinstance(gemini_err, AppError)
    assert gemini_err.status_code == 429
    assert gemini_err.code == "GEMINI_RATE_LIMITED"
    assert gemini_err.details == {"rpm_limit": 60}


def test_fastapi_typed_exception_handling():
    """Integration test: verify FastAPI routes raising typed errors return correct HTTP status and JSON shape."""
    test_app = FastAPI()
    setup_exception_handlers(test_app)

    @test_app.get("/test-not-found")
    def route_not_found():
        raise NotFoundError("Project #123 not found")

    @test_app.get("/test-rate-limited")
    def route_rate_limited():
        raise RateLimitedError()

    client = TestClient(test_app)

    res1 = client.get("/test-not-found")
    assert res1.status_code == 404
    assert res1.json() == {
        "error": {
            "code": "NOT_FOUND",
            "message": "Project #123 not found",
            "details": None,
        }
    }

    res2 = client.get("/test-rate-limited")
    assert res2.status_code == 429
    assert res2.json() == {
        "error": {
            "code": "RATE_LIMITED",
            "message": "Rate limit exceeded. Please try again later.",
            "details": None,
        }
    }


def test_unhandled_exception_hides_internal_traceback():
    """Security test: verify unhandled server exceptions return safe 500 JSON without leaking stack traces or internal secrets."""
    test_app = FastAPI()
    setup_exception_handlers(test_app)

    @test_app.get("/test-crash")
    def route_crash():
        raise RuntimeError("Database connection string postgresql://user:secret_pass@db:5432 failed")

    client = TestClient(test_app, raise_server_exceptions=False)
    res = client.get("/test-crash")

    assert res.status_code == 500
    body = res.json()

    assert body == {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please contact support.",
            "details": None,
        }
    }
    # Ensure sensitive string is never exposed to client
    assert "secret_pass" not in res.text
    assert "RuntimeError" not in res.text
    assert "Traceback" not in res.text
