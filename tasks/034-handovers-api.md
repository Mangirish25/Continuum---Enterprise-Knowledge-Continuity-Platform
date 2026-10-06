# Task 034 — `apps/api/app/api/v1/handovers.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 033 (state machine), Task 009/010 (auth)
**Requirements:** REQ-P004
**Board ref:** `tasks/BOARD.md` — Phase 10.2
**Owner:** Sanmati

## Goal

The HTTP surface for the handover workflow — initiate, view status, transition, approve — following the established pattern from Task 013.

## Scope

- `apps/api/app/api/v1/handovers.py`
- Endpoints to initiate a handover, view its current state/history, trigger valid transitions (via Task 033), and record approvals (`handover_approvals`).
- Same auth/authorization/error/schema conventions as Task 013.

## Out of scope

- Successor recommendation generation — reads Task 036's output once it exists; doesn't generate it itself.
- Access-transfer execution logic — calls into Task 038.

## Implementation notes

- Follow Task 013's established pattern exactly, same as Task 014 did — read its real implementation rather than re-deriving conventions independently.

## Acceptance criteria

- [ ] Full handover lifecycle is drivable via these endpoints end-to-end (initiate → transitions → approval → closure), respecting Task 033's enforced rules.
- [ ] An unauthorized user cannot trigger a transition or approval they're not permitted to make.
- [ ] Errors follow the established typed-exception → structured-response pattern.

## Tests

- [ ] Unit — request/response schema validation
- [ ] Integration — full handover flow against a real running stack
- [ ] Security — unauthorized transition/approval attempts are rejected
- [ ] E2E — the first full handover lifecycle test, end-to-end through HTTP

## Documentation updates

`docs/API.md` — document these endpoints.

## Known limitations

_Fill in at completion._
