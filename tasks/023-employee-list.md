# Task 023 — `apps/web/src/features/employees/EmployeeList.tsx`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 010 (auth API — for user data), Task 020 (AppShell)
**Requirements:** REQ-P001
**Board ref:** `tasks/BOARD.md` — Phase 6.7
**Owner:** Rahul

## Goal

A view of organization members/employees — the knowledge-continuity platform's other core entity alongside projects.

## Scope

- `apps/web/src/features/employees/EmployeeList.tsx`
- List users within the organization with basic profile info (name, role, team — whatever Task 007's `users`/`roles`/`teams` tables expose via an endpoint; if no dedicated employees endpoint exists yet, flag this as a gap rather than building against data that doesn't exist).

## Out of scope

- Skill/ownership mapping visualization — later refinement once risk/succession data (Phase 9/11) exists to connect to.
- Editing user roles/permissions from this page — that's an admin concern (Task 055), not this list view.

## Implementation notes

- There is currently no dedicated `api/v1/employees.py` or equivalent task on the board — confirm with Sanmati whether user-listing is exposed through an existing endpoint (e.g. an admin/org-members endpoint) before building this, rather than assuming one exists.

## Acceptance criteria

- [ ] Employee list renders real organization members from a confirmed real endpoint.
- [ ] If no such endpoint exists yet, this is flagged explicitly rather than silently built against placeholder data and left that way.

## Tests

- [ ] Unit — component renders given sample data
- [ ] Integration — loads real org members if an endpoint exists
- [ ] Security — n/a beyond server-side org scoping
- [ ] E2E — n/a

## Documentation updates

Flag the missing employees-listing endpoint as a gap if confirmed absent — this may need a small addition to Phase 4's `api/v1/` scope.

## Known limitations

_Fill in at completion — note explicitly whether a real backend endpoint existed for this or whether it's still blocked on one._
