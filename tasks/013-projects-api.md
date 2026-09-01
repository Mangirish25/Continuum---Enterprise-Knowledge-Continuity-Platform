# Task 013 — `apps/api/app/api/v1/projects.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 011 (project repository), Task 009 (`core/security.py` — auth/RBAC dependencies), Task 010 (auth API — needs a working login to test against)
**Requirements:** REQ-P002, REQ-S001
**Board ref:** `tasks/BOARD.md` — Phase 4.3
**Owner:** Sanmati

## Goal

The first real authenticated business-logic API — CRUD and ownership endpoints for projects, callable by Rahul's frontend (Phase 6) and exercising the full stack built so far (auth → RBAC → repository → database).

## Scope

- `apps/api/app/api/v1/projects.py`
- REST endpoints: create/list/get/update/delete project, add/remove/list members, transfer or change ownership (current-owner concept only — not the handover *workflow*, see Out of scope).
- Every endpoint requires authentication (Task 009/010) and enforces organization + role/membership authorization before touching Task 011's repository.
- Request/response schemas (Pydantic) that don't leak internal fields (e.g. no raw ORM objects returned directly).
- Errors surfaced via Task 006's typed exception → structured response mapping.

## Out of scope

- The handover state machine and `ownership_transfers` table — Phase 10. "Ownership" here means "who is currently marked as owner," a simple field update with an authorization check; it is not the controlled, human-approved handover process.
- Risk/bus-factor data on the response — Phase 9 adds that once it exists; don't stub fake risk fields now.
- Pagination/filtering sophistication beyond what's reasonable for an MVP list endpoint (basic limit/offset or cursor is fine — don't over-build this).

## Implementation notes

- This is the reference implementation for "authenticated CRUD endpoint" in this codebase — Task 014 (`assets.py`) and later Phase 9–10 endpoints will likely follow its shape. Get the auth-dependency wiring, error handling, and schema conventions right here rather than each later task reinventing them slightly differently.
- Test this against a real running stack (Task 003 compose + Task 008 migration applied + Task 010 login working) — this is the first task where "does the whole thing actually work together" becomes a meaningful question, not just "does this file's logic work in isolation."

## Acceptance criteria

- [ ] All CRUD + membership + ownership endpoints work end-to-end against a real running stack.
- [ ] Every endpoint rejects unauthenticated requests and requests from a user without appropriate organization/role/membership permissions.
- [ ] Response schemas contain only intended fields — no accidental leakage of internal/other-organization data.
- [ ] Errors return structured responses via Task 006, with correct HTTP status codes.
- [ ] A full flow works manually or via test: login (Task 010) → create project → add member → update → verify a user from a different organization cannot see or modify it.

## Tests

- [ ] Unit — request/response schema validation
- [ ] Integration — full authenticated CRUD flow against a real stack
- [ ] Security — cross-organization and insufficient-role access attempts are all rejected; verified explicitly, not assumed from Task 011's repository tests alone
- [ ] E2E — this is the first genuinely end-to-end business-logic path in the system; treat it as the reference E2E test for the pattern

## Documentation updates

- `docs/API.md` — document these endpoints (paths, methods, request/response shapes, auth requirements) as the first real business-logic HTTP contract.

## Known limitations

_Fill in at completion._
