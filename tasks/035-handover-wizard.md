# Task 035 — `apps/web/src/features/handover/HandoverWizard.tsx`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 034 (handovers API)
**Requirements:** REQ-P004, REQ-P001
**Board ref:** `tasks/BOARD.md` — Phase 10.3
**Owner:** Rahul

## Goal

A guided UI walking a user through initiating and progressing a handover, reflecting Task 033's state machine so the UI can't attempt an invalid transition either.

## Scope

- `apps/web/src/features/handover/HandoverWizard.tsx`
- A step-by-step flow matching the state machine's stages, showing current state, available next actions, and approval status.
- Mirrors (doesn't duplicate independently) Task 033's valid-transition rules so the UI only ever offers actions the backend will actually accept — if the backend rejects something the UI offered, that's a bug in this task, not an acceptable UX gap.

## Out of scope

- Successor recommendation display logic — depends on Task 036; wire this in once that exists, not before.

## Implementation notes

- Build the wizard shell and state-tracking first against Task 034's real endpoints; a graceful 'coming soon' state for the still-unbuilt successor-recommendation step (Task 036) is fine as a temporary placeholder here, same pattern as Task 021's dashboard placeholders.

## Acceptance criteria

- [ ] A user can walk through the full handover flow Task 034 supports, with the UI only offering valid next actions at each state.
- [ ] Approval status and current state are always accurately reflected from the real backend, not assumed client-side.

## Tests

- [ ] Unit — component renders correct available actions given a sample state
- [ ] Integration — full wizard flow against a real running Task 034 backend
- [ ] Security — n/a beyond what Task 034 enforces server-side
- [ ] E2E — initiate → progress through states → approve → closure, against the real stack

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
