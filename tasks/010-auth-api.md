# Task 010 — `apps/api/app/api/v1/auth.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 009 (`core/security.py`), Task 006 (`core/exceptions.py` — for typed error responses)
**Requirements:** REQ-S001 (enforce organization/resource authorization server-side)
**Board ref:** `tasks/BOARD.md` — Phase 3.2
**Owner:** Sanmati

## Goal

The HTTP-facing login/refresh/logout endpoints that let a client (Rahul's frontend, Phase 6) actually obtain and use a token — the first real API surface in the system, and the thing every other authenticated route (Phase 4 onward) will be tested against.

## Scope

- `apps/api/app/api/v1/auth.py`
- Login endpoint (credential or dev-mode path per Task 009's decision) issuing access + refresh tokens via `core/security.py`.
- Token refresh endpoint.
- Logout/token-revocation endpoint if refresh tokens are stateful (if refresh tokens are stateless/short-lived by design instead, document that choice here rather than building revocation for nothing).
- Error responses go through Task 006's typed exceptions — invalid credentials, expired/invalid tokens, and rate-limited login attempts (if implemented) all return structured, non-leaky responses (`docs/SECURITY.md` — failed authentication should be monitorable, not silently swallowed either).

## Out of scope

- User registration/self-signup flows — not in `docs/REQUIREMENTS.md` as a stated requirement; if needed later it's a separate task.
- OIDC/SAML — same as Task 009, deferred.
- Rate-limiting login attempts against brute force — worth flagging in "Known limitations" if skipped, but not required to block this task if time-constrained; note it rather than silently omitting it.

## Implementation notes

- This is the first endpoint a teammate or the frontend will actually call — treat "does this work cleanly from a fresh `docker compose up`" as part of the bar, not just unit-level correctness.
- `docs/SECURITY.md` §Monitoring lists "failed authentication" as something that should be monitorable — at minimum, make sure failed attempts are logged in a way that could support that later, even if full monitoring infra is out of scope now.

## Acceptance criteria

- [ ] A valid credential/dev-mode login returns a usable access + refresh token pair.
- [ ] An invalid login attempt returns a structured 401-class error via Task 006's exception hierarchy, not a raw error.
- [ ] Token refresh works and correctly rejects an expired/invalid refresh token.
- [ ] Logout/revocation behaves as documented (or is explicitly documented as unnecessary given a stateless design).
- [ ] End-to-end: login → use token against a simple protected test route (built for this task or reused from Task 009's tests) → succeeds; using an invalid/expired token → fails with a structured error.

## Tests

- [ ] Unit — request/response validation for each endpoint
- [ ] Integration — full login → protected-route → refresh → protected-route flow against a running Task-003/008 stack
- [ ] Security — invalid credentials, expired tokens, tampered tokens, and wrong-organization tokens are all rejected; no sensitive detail leaks in error responses
- [ ] E2E — this is effectively the first real E2E path in the system; treat it as such

## Documentation updates

- `docs/API.md` — document the actual auth endpoints (paths, request/response shapes) once implemented, since this is the first concrete HTTP contract in the system.

## Known limitations

_Fill in at completion — e.g. whether brute-force protection was implemented or deferred._
