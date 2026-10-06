# Task 021 — `apps/web/src/pages/Dashboard.tsx`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 020 (AppShell)
**Requirements:** REQ-P001 (dashboards)
**Board ref:** `tasks/BOARD.md` — Phase 6.5
**Owner:** Rahul

## Goal

A landing page giving an at-a-glance view once a user logs in — can be built with placeholder/synthetic data ahead of Phase 9's real risk metrics.

## Scope

- `apps/web/src/pages/Dashboard.tsx`
- Summary widgets: project count, recent activity, and placeholders for continuity-risk summary (real data arrives in Phase 9) and pending handovers (Phase 10) — wire these to real endpoints as they land rather than leaving permanent dead stubs.

## Out of scope

- Actual bus-factor/KCS calculations — Phase 9 supplies the real data this page will eventually consume.
- Customizable/configurable dashboards — a fixed layout is sufficient for the current scope.

## Implementation notes

- Use clearly-labeled synthetic/placeholder data for anything not yet backed by a real endpoint (Phase 9/10), and revisit this task when those land rather than letting stale fake numbers ship as if real — this directly matters for `docs/DEMO.md`'s demo-stability principle once this becomes viva-facing.

## Acceptance criteria

- [ ] Page renders cleanly for an authenticated user with real project data (Task 013/022).
- [ ] Any placeholder sections are clearly marked as such internally (e.g. a TODO linking to the Phase 9/10 task) so they aren't mistaken for finished features.

## Tests

- [ ] Unit — widgets render given sample data
- [ ] Integration — page loads real project counts from Task 013's API
- [ ] Security — n/a
- [ ] E2E — n/a

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
