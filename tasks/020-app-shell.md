# Task 020 — `apps/web/src/components/layout/AppShell.tsx`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 019 (useAuth — needs to know who's logged in to render nav)
**Requirements:** REQ-P001 (dashboards, projects, employees, knowledge assistant, handover screens, admin interfaces)
**Board ref:** `tasks/BOARD.md` — Phase 6.4
**Owner:** Rahul

## Goal

The layout scaffold (nav, shell) every other frontend page renders inside, so each feature doesn't rebuild navigation independently.

## Scope

- `apps/web/src/components/layout/AppShell.tsx`
- Navigation covering the areas the Guide and `docs/REQUIREMENTS.md` call for: Dashboard, Projects, Employees, Knowledge Assistant, Risk, Handover, Admin.
- Role-aware nav (e.g. Admin section only visible to appropriate roles, using Task 019's exposed user/role info) — doesn't need full enforcement here (the backend enforces authorization regardless), but shouldn't visibly offer actions a user can't actually perform.
- Routing scaffold wiring each nav item to its page/feature (even if some pages are still placeholders at this point in the build).

## Out of scope

- Actual feature content for each page — those are Tasks 021–023, 029, 032, 035, 055.
- Visual design system/branding decisions beyond what's needed for a clean, usable layout — treat this as functional scaffolding, not a polish pass.

## Implementation notes

- This is the first thing every teammate (and eventually the viva audience) sees — keep it simple and working rather than over-engineered; `docs/DEMO.md`'s demo-stability principle extends to the UI, not just the backend.
- Every later Phase 6+ page assumes this shell exists — get its route/layout contract stable early so later tasks aren't redoing navigation wiring.

## Acceptance criteria

- [ ] Nav covers Dashboard, Projects, Employees, Knowledge Assistant, Risk, Handover, Admin.
- [ ] Logged-out users are redirected to login rather than seeing the shell.
- [ ] Nav doesn't visibly offer sections a user's role shouldn't see, based on Task 019's user/role info.
- [ ] Routing is wired so each nav item goes somewhere real (even a placeholder page), not a dead link.

## Tests

- [ ] Unit — nav renders correct items based on auth/role state
- [ ] Integration — navigating between sections works and preserves auth state
- [ ] Security — n/a beyond what Task 019 already covers (this is UI-level hiding, not the enforcement boundary)
- [ ] E2E — logged-out → redirected; logged-in → can reach every nav destination

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
