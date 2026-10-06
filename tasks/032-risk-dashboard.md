# Task 032 — `apps/web/src/features/risk/RiskDashboard.tsx`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 030/031 (real risk data), Task 013 (projects API, for project context)
**Requirements:** REQ-A002, REQ-P001
**Board ref:** `tasks/BOARD.md` — Phase 9.3
**Owner:** Rahul

## Goal

Surfaces Task 030/031's deterministic risk scores to users — replaces Task 021's Dashboard placeholder risk section with real data.

## Scope

- `apps/web/src/features/risk/RiskDashboard.tsx`
- Per-project bus-factor/KCS display, plus any documentation-staleness signal from Task 031.
- Links back into Task 021's Dashboard summary once real data exists (replace the placeholder noted in that task).

## Out of scope

- Natural-language explanations of why a score is what it is — that's the Risk Agent's territory (Task 041) if/when it's surfaced in the UI; this task shows the deterministic numbers and their documented inputs, not an AI narrative.

## Implementation notes

- Go back and update Task 021's Dashboard placeholder once this is built, so the two don't silently diverge (one showing fake data, one showing real data, with no one noticing).

## Acceptance criteria

- [ ] Risk scores displayed are real, computed values from Task 030/031, not placeholders.
- [ ] Task 021's Dashboard is updated to link to or embed this real data instead of its placeholder.

## Tests

- [ ] Unit — component renders given sample risk data
- [ ] Integration — loads real risk scores from the backend
- [ ] Security — n/a beyond standard org-scoped data access
- [ ] E2E — n/a

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
