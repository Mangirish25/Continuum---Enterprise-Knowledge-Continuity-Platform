# Task 022 — `apps/web/src/features/projects/ProjectList.tsx`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 013 (`api/v1/projects.py`), Task 020 (AppShell)
**Requirements:** REQ-P001, REQ-P002
**Board ref:** `tasks/BOARD.md` — Phase 6.6
**Owner:** Rahul

## Goal

The first real data-backed feature page — list, view, and manage projects through Task 013's API.

## Scope

- `apps/web/src/features/projects/ProjectList.tsx` (plus a project-detail view if not better split into its own file — use judgment, following whatever pattern `docs/IMPLEMENTATION_STRUCTURE.md` implies for feature-folder organization).
- List projects (scoped to the user's organization automatically, since Task 013's API already enforces that server-side).
- Create/edit/delete actions calling Task 013's endpoints, with clear error surfacing (using Task 017's client error shape) when an action fails (e.g. insufficient permissions).

## Out of scope

- Risk/bus-factor display on this page — Phase 9 adds that; don't fabricate placeholder risk numbers here, just omit the field until it's real.
- Advanced filtering/search beyond basic list display — keep MVP scope.

## Implementation notes

- This is the reference implementation for 'frontend feature page talking to a real authenticated API' — Task 023 and later feature pages will likely follow its shape. Worth getting the loading/error/empty states right here once rather than inconsistently per page.

## Acceptance criteria

- [ ] Projects list loads from Task 013's real API for an authenticated user.
- [ ] Create/edit/delete work end-to-end against the real backend.
- [ ] A permission-denied response from the backend is surfaced clearly to the user, not silently swallowed.
- [ ] Loading and empty states are handled (not just the happy path).

## Tests

- [ ] Unit — component renders given sample API responses, including error/empty states
- [ ] Integration — full CRUD flow against a real running Task 013 backend
- [ ] Security — n/a beyond what Task 013 already enforces server-side
- [ ] E2E — login → view projects → create → edit → delete, against the real stack

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
