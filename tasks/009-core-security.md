# Task 009 — `apps/api/app/core/security.py`

**Status:** backlog
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
- Password hashing/verification if local credential auth is in scope for the current phase (confirm against `docs/REQUIREMENTS.md`/`docs/SECURITY.md` — if enterprise IdP/OIDC is the primary path per `docs/SECURITY.md` §Identity, local password auth may only be needed for dev/demo login; implement whichever is actually needed for Task 010 to work, and note the choice here).
- RBAC permission-check helpers/dependencies that a route can use to enforce: authenticated identity → organization boundary → role permissions → project/resource membership (the first three layers of `docs/SECURITY.md`'s six; classification/ACL and RLS are later-phase concerns tied to knowledge retrieval and are out of scope here).
- A documented extension point for MFA (`docs/SECURITY.md` — "MFA where applicable") — doesn't need to be implemented now, but the token/session shape shouldn't have to be redesigned to add it later.

## Out of scope

- OIDC/SAML enterprise identity provider integration itself — `docs/SECURITY.md` lists this as a path, but wiring an actual external IdP is a separate task once one is prioritized. This task should not block on it.
- Classification/ACL-based authorization and RLS — those are tied to knowledge retrieval (Phase 8) and should be layered on top of this, not built here.
- MFA implementation — extension point only, per above.

## Implementation notes

- This is the layer everything downstream trusts. Treat it with the same conservatism as Task 007 — prefer well-understood patterns over cleverness.
- `docs/SECURITY.md` says "development `.env` is acceptable for local use; production uses a secret-management/deployment mechanism" — the JWT signing secret must come through Task 005's config module, never a literal string in this file.
- Coordinate with Task 007's `users`/`roles`/`user_roles` shape rather than assuming a structure — if something's missing (e.g. a field needed for a JWT claim), that's a signal to revisit Task 007, not to work around it here.

## Acceptance criteria

- [ ] Tokens are issued and verified correctly; a tampered or expired token is rejected with a typed error (`core/exceptions.py`, Task 006), not a raw exception.
- [ ] No JWT signing secret is hardcoded anywhere — it's read via Task 005's config, and there's no unsafe default outside dev mode.
- [ ] RBAC helpers can answer "is this user authorized for this organization/role/project-membership combination" without a route having to hand-roll that logic itself.
- [ ] The MFA extension point is documented (even if unimplemented) so it doesn't require a breaking change later.

## Tests

- [ ] Unit — token issuing/verification, expiry handling, tampered-token rejection, RBAC helper logic against various role/org/membership combinations
- [ ] Integration — a protected test route correctly allows/denies based on token + RBAC state
- [ ] Security — confirm no secret defaults outside dev mode; confirm expired/tampered/wrong-organization tokens are all rejected, not just missing ones
- [ ] E2E — deferred to Task 010 (`api/v1/auth.py`), which exercises this end-to-end via HTTP

## Documentation updates

- `docs/SECURITY.md` — update if the actual implementation resolves an open question it left ambiguous (e.g. whether local password auth exists alongside/instead of OIDC).

## Known limitations

_Fill in at completion — e.g. confirm whether OIDC/SAML remains a documented future path or an active near-term one._
