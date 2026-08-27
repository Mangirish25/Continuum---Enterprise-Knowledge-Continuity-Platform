# Task 006 — `apps/api/app/core/exceptions.py`

**Status:** done
**Priority:** P0
**Depends on:** none (should land alongside Task 005 — they reference each other)
**Requirements:** supports REQ-R003 (external integration failures do not corrupt domain state); enables typed error handling referenced throughout `AGENTS.md`
**Board ref:** `tasks/BOARD.md` — Phase 1.6
**Owner:** Sanmati

## Goal

A base set of typed application exceptions and an API-layer error handler so every error surfaced to a client is a professional, structured response — never a raw exception message or bare HTTP status code (`AGENTS.md` coding style: "structured errors").

## Scope

- `apps/api/app/core/exceptions.py`
- A small hierarchy of typed exceptions, e.g.: `AppError` (base), `NotFoundError`, `AuthorizationError`, `ValidationError`, `ConflictError`, `RateLimitedError`, `UpstreamIntegrationError` — enough to cover Phase 1–7 needs without over-engineering a taxonomy nobody uses yet.
- Each exception carries a stable machine-readable error code and a human-readable message, separate from any internal detail (stack trace, raw upstream error body) that must never leak to the client.
- A FastAPI exception handler (can live here or in `apps/api/app/api/`, but reference it from this task) that converts these typed exceptions into a consistent JSON error shape.
- Leave a documented extension point for the future `GeminiLimitError` (already implemented in `gemini_rate_limiter.py`) to plug into this hierarchy rather than being a one-off — confirm it can subclass `RateLimitedError` or similar without modification to the limiter itself.

## Out of scope

- Domain-specific exceptions for modules that don't exist yet (handover, risk, etc.) — those get added by the tasks that introduce those modules, following this file's pattern.
- Retry/idempotency logic itself (Phase-later concern) — this task only covers how an eventual failure is *reported*, not retried.

## Implementation notes

- Implemented `apps/api/app/core/exceptions.py` containing `AppError` base class and derived exception hierarchy (`NotFoundError`, `AuthorizationError`, `AuthenticationError`, `ValidationError`, `ConflictError`, `RateLimitedError`, `UpstreamIntegrationError`).
- Implemented `app_error_handler`, `unhandled_exception_handler`, and `setup_exception_handlers` for FastAPI.
- Connected `ConfigurationError` in `apps/api/app/core/config.py` to inherit from `AppError`.
- Verified `GeminiLimitError` in Phase 8 can seamlessly subclass `RateLimitedError`.
- Registered `setup_exception_handlers(app)` in `apps/api/app/main.py`.
- Tested in `apps/api/tests/test_exceptions.py` (4 passed, 9 total backend tests passing).

## Acceptance criteria

- [x] A base `AppError` exists with a stable `code` and safe `message`.
- [x] At minimum `NotFoundError`, `AuthorizationError`, `ValidationError`, `ConflictError`, `RateLimitedError`, `UpstreamIntegrationError` are defined.
- [x] A FastAPI handler maps these to a consistent JSON error response shape and appropriate HTTP status codes.
- [x] An unexpected/unhandled exception is still caught and returned as a generic safe error — never a raw traceback to the client.
- [x] The existing `GeminiLimitError` can reasonably integrate with this hierarchy without changes to `gemini_rate_limiter.py`.

## Tests

- [x] Unit — each exception type maps to the correct status code and response shape; unhandled exceptions are caught safely (`apps/api/tests/test_exceptions.py`)
- [x] Integration — a route that raises each exception type returns the expected structured response (`apps/api/tests/test_exceptions.py`)
- [x] Security — confirmed no internal detail (stack trace, upstream raw body, secret values) ever appears in a response body
- [ ] E2E — n/a yet

## Documentation updates

- None required — operationalizes `AGENTS.md` structured errors requirement.

## Known limitations

- Domain-specific exceptions for future modules (e.g., HandoverStateError in Phase 10) will subclass `AppError` when those modules are built.
