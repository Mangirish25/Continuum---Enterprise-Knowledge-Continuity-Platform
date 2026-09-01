# Task 011 — `apps/api/app/repositories/project_repository.py`

**Status:** backlog
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

- This is the first repository in the codebase — the patterns established here (how organization scoping is enforced, how pagination/filtering works, how errors map to Task 006's typed exceptions) will likely be copied by Task 012 (`asset_repository.py`) and every later repository. Keep it clean and consistent rather than optimizing this one file in isolation.
- A `NotFoundError` (Task 006) for a project that doesn't exist or isn't in the caller's organization should look identical from the caller's perspective — don't leak "it exists but you can't see it" vs. "it doesn't exist" (this is a standard authorization hygiene practice, consistent with `docs/SECURITY.md`'s layered authorization model).

## Acceptance criteria

- [ ] Full CRUD for projects, scoped to organization.
- [ ] Membership add/remove/list works and is also organization-scoped.
- [ ] No method allows querying or mutating a project outside the caller's organization, even if given a valid project ID from another org.
- [ ] Errors map to Task 006's typed exceptions (`NotFoundError`, `ConflictError`, etc.), not raw ORM exceptions leaking upward.

## Tests

- [ ] Unit — repository logic against a test database: CRUD correctness, membership operations
- [ ] Integration — cross-organization isolation is explicitly tested (create project in org A, confirm org B's repository calls cannot see or modify it)
- [ ] Security — the cross-org isolation test above is the security-relevant one; treat it as mandatory, not optional
- [ ] E2E — deferred to Task 013

## Documentation updates

- None expected unless the repository reveals a gap in Task 007's schema (e.g. a missing column needed for a real query) — if so, go back and fix Task 007's models/migration rather than working around it here.

## Known limitations

_Fill in at completion._
