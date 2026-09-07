# Task 011 — `apps/api/app/repositories/project_repository.py`

**Status:** done
**Priority:** P0
**Depends on:** Task 007 (ORM models), Task 008 (initial migration — needs real tables to query against)
**Requirements:** REQ-P002 (track users, projects, assets, ownership and continuity metadata), REQ-S001 (enforce organization/resource authorization server-side)
**Board ref:** `tasks/BOARD.md` — Phase 4.1
**Owner:** Sanmati

## Goal

The data-access layer for projects — every query that touches the `projects`/`project_members`/`project_dependencies` tables goes through this repository, not through ad hoc queries scattered across route handlers.

## Scope

- `apps/api/app/repositories/project_repository.py`
- CRUD operations against `projects` (create, get by id, list, update, soft/hard delete per Task 007's documented deletion policy).
- Membership operations against `project_members` (add/remove/list members, role-within-project if applicable).
- Dependency operations against `project_dependencies` (record/list a project's dependencies on other projects, if that's part of the current data model — check Task 007's actual schema rather than assuming).
- Every query scoped by `organization_id` (`docs/DATABASE.md` §3) — this repository must make it structurally hard to accidentally query across organizations, e.g. every method takes an `organization_id` (or an already-scoped session/context) rather than trusting the caller to filter correctly.

## Out of scope

- HTTP-layer concerns (auth checks, request/response schemas) — that's Task 013 (`api/v1/projects.py`), which depends on this.
- Ownership *transfer* logic tied to handovers — that's `ownership_transfers` and belongs to the handover workflow (Phase 10), not this task. This task's "ownership" scope is limited to who currently owns/is a member of a project, not the transfer process.
- Risk/bus-factor calculations that read project data — those are Phase 9, reading through this repository rather than duplicating its queries.

## Implementation notes

- Implemented `ProjectRepository` in `apps/api/app/repositories/project_repository.py`.
- Enforces strict multi-tenant isolation on every method using `organization_id`.
- Mapped all ORM and integrity exceptions to typed exceptions (`NotFoundError`, `ConflictError`, `ValidationError`, `AppError`) from Task 006 (`apps/api/app/core/exceptions.py`).
- Validated cross-tenant isolation and data access hygiene: querying or mutating a project or resource outside the caller's organization yields identical `NotFoundError` without leaking existence.
- Created 27 unit, integration, and security tests in `apps/api/tests/test_project_repository.py`. All 60 backend tests pass.

## Acceptance criteria

- [x] Full CRUD for projects, scoped to organization.
- [x] Membership add/remove/list works and is also organization-scoped.
- [x] No method allows querying or mutating a project outside the caller's organization, even if given a valid project ID from another org.
- [x] Errors map to Task 006's typed exceptions (`NotFoundError`, `ConflictError`, etc.), not raw ORM exceptions leaking upward.

## Tests

- [x] Unit — repository logic against a test database: CRUD correctness, membership operations
- [x] Integration — cross-organization isolation is explicitly tested (create project in org A, confirm org B's repository calls cannot see or modify it)
- [x] Security — the cross-org isolation test above is the security-relevant one; treat it as mandatory, not optional
- [ ] E2E — deferred to Task 013

## Documentation updates

- None required — model definitions strictly match Task 007 models and schema.

## Known limitations

- Direct self-dependencies and duplicate dependencies are rejected at the repository boundary; complex multi-hop circular dependency chain analysis (e.g. A -> B -> C -> A) is left to domain service layers in Phase 9/10.
- Synchronous SQLAlchemy `Session` interface is used matching current `core/database.py` session management.

