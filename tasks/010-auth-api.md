# Task 010 — `apps/api/app/api/v1/auth.py`

**Status:** done
**Priority:** P0
**Depends on:** Task 009 (`core/security.py`), Task 006 (`core/exceptions.py` — for typed error responses)
**Requirements:** REQ-S001 (enforce organization/resource authorization server-side)
**Board ref:** `tasks/BOARD.md` — Phase 3.2
**Owner:** Sanmati

## Goal

The HTTP-facing login/refresh/logout endpoints that let a client (Rahul's frontend, Phase 6) actually obtain and use a token — the first real API surface in the system, and the thing every other authenticated route (Phase 4 onward) will be tested against.

## Scope

- `apps/api/app/api/v1/auth.py`
- Login endpoint issuing access + refresh tokens via `core/security.py`.
- Token refresh endpoint.
- Logout endpoint (stateless tokens).
- Error responses go through Task 006's typed exceptions — invalid credentials and expired/invalid tokens return structured non-leaky responses; failed authentication attempts are logged for monitoring (`docs/SECURITY.md`).

## Out of scope

- User registration/self-signup flows — not in `docs/REQUIREMENTS.md`.
- OIDC/SAML — deferred.
- Rate-limiting login attempts against brute force — noted in Known limitations.

## Implementation notes

- Created Auth API endpoints router in `apps/api/app/api/v1/auth.py`.
- Registered `auth_router` in `apps/api/app/main.py` under `/api/v1`.
- Added E2E and unit tests in `apps/api/tests/test_auth_api.py` (7 passed, 33 total backend tests passing).
- Documented Auth HTTP schemas in `docs/API.md`.

## Acceptance criteria

- [x] A valid credential/dev-mode login returns a usable access + refresh token pair.
- [x] An invalid login attempt returns a structured 401-class error via Task 006's exception hierarchy, not a raw error.
- [x] Token refresh works and correctly rejects an expired/invalid refresh token.
- [x] Logout/revocation behaves as documented (stateless JWT tokens).
- [x] End-to-end: login → use token against a protected test route → succeeds; using an invalid/expired token → fails with a structured error.

## Tests

- [x] Unit — request/response validation for each endpoint (`apps/api/tests/test_auth_api.py`)
- [x] Integration — full login → protected-route → refresh → protected-route flow against database/test stack (`apps/api/tests/test_auth_api.py`)
- [x] Security — invalid credentials, expired tokens, tampered tokens, and wrong-organization tokens are all rejected; no sensitive detail leaks in error responses (`apps/api/tests/test_auth_api.py`)
- [x] E2E — verified end-to-end auth path in `apps/api/tests/test_auth_api.py`

## Documentation updates

- `docs/API.md` — documented `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout` endpoints with exact request and response JSON schemas.

## Known limitations

- Rate-limiting login attempts against brute-force attacks is deferred to Phase 5 worker/security rate limiting policies; failed login attempts log warnings for security monitoring.

