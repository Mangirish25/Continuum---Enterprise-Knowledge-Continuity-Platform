# Task 009 — `apps/api/app/core/security.py`

**Status:** done
**Priority:** P0
**Depends on:** Task 007 (ORM models — needs `users`/`roles`/`user_roles`), Task 005 (`core/config.py` — needs JWT signing config)
**Requirements:** REQ-S001 (enforce organization/resource authorization server-side), `docs/SECURITY.md` §Identity, §Authorization
**Board ref:** `tasks/BOARD.md` — Phase 3.1
**Owner:** Sanmati

## Goal

The JWT issuing/verification and RBAC permission-checking primitives that every authenticated route in the backend depends on — this is the enforcement point `docs/SECURITY.md`'s six-layer authorization model builds on.

## Scope

- `apps/api/app/core/security.py`
- JWT issuing (access token, refresh token) and verification, using config from Task 005 (no hardcoded signing secret, ever, in any environment).
- Password hashing/verification via `bcrypt` for local dev/demo login alongside enterprise IdP mapping fields (`external_identity_provider`, `external_identity_id`).
- RBAC permission-check helpers/dependencies enforcing authenticated identity → organization boundary → role permissions → project/resource membership (first three layers of `docs/SECURITY.md`'s six).
- Documented extension point for MFA (`mfa_verified: bool`, `amr: list[str]` claims in tokens).

## Out of scope

- OIDC/SAML enterprise identity provider integration itself — separate task once an external IdP is prioritized.
- Classification/ACL-based authorization and RLS — tied to knowledge retrieval (Phase 8).
- Full MFA flow implementation — token extension point only.

## Implementation notes

- Created security primitives module in `apps/api/app/core/security.py`.
- All token verification failures raise typed `AuthenticationError` (401) from `apps.api.app.core.exceptions` (no raw JWT exceptions leaked).
- All RBAC and organization boundary failures raise typed `AuthorizationError` (403).
- Added unit and HTTP integration tests in `apps/api/tests/test_security.py` (10 passed, 26 total backend tests passing).
- Updated `docs/SECURITY.md` documenting local password auth and MFA claim extension points.

## Acceptance criteria

- [x] Tokens are issued and verified correctly; a tampered or expired token is rejected with a typed error (`core/exceptions.py`, Task 006), not a raw exception.
- [x] No JWT signing secret is hardcoded anywhere — it's read via Task 005's config, and there's no unsafe default outside dev mode.
- [x] RBAC helpers can answer "is this user authorized for this organization/role/project-membership combination" without a route having to hand-roll that logic itself.
- [x] The MFA extension point is documented (`mfa_verified` & `amr` claims) so it doesn't require a breaking change later.

## Tests

- [x] Unit — token issuing/verification, expiry handling, tampered-token rejection, RBAC helper logic against various role/org/membership combinations (`apps/api/tests/test_security.py`)
- [x] Integration — a protected test route correctly allows/denies based on token + RBAC state (`apps/api/tests/test_security.py`)
- [x] Security — confirm no secret defaults outside dev mode; confirm expired/tampered/wrong-organization tokens are all rejected, not just missing ones (`apps/api/tests/test_security.py`)
- [ ] E2E — deferred to Task 010 (`api/v1/auth.py`), which exercises this end-to-end via HTTP

## Documentation updates

- `docs/SECURITY.md` — updated Identity section documenting local bcrypt password auth and MFA claim extension point.

## Known limitations

- Direct enterprise OIDC/SAML OAuth flow handling is deferred to future identity provider tasks; user model preserves `external_identity_provider` and `external_identity_id` fields.

