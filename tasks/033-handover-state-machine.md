# Task 033 — `apps/api/app/modules/handover/state_machine.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 011 (project repository), Task 015 (audit ledger — handover transitions must be audited)
**Requirements:** REQ-P004 (create a knowledge package and transfer plan when an employee leaves/changes role), ADR-008 (formal handover state machine)
**Board ref:** `tasks/BOARD.md` — Phase 10.1
**Owner:** Sanmati

## Goal

The explicit states and allowed transitions for a handover's lifecycle, per ADR-008 — 'Handover lifecycle is represented as explicit states and allowed transitions,' not an implicit status field.

## Scope

- `apps/api/app/modules/handover/state_machine.py`
- States covering the Guide's documented flow: initiated → knowledge/ownership collected → gaps identified → handover package built → successor recommended → approver review → ownership/access transferred → verified → closed (adjust exact naming to match `docs/HANDOVER.md` if it specifies one — read it before finalizing state names).
- Enforced transition rules — an invalid transition (e.g. skipping approval) must be rejected with a typed error (Task 006), not silently allowed.
- Every transition writes an audit event via Task 015 — this is exactly the kind of sensitive operation ADR-007's ledger exists for.

## Out of scope

- The actual `api/v1/handovers.py` HTTP surface — Task 034, which wraps this state machine.
- Successor recommendation logic itself — Task 036 (Succession Agent); this task only enforces that a recommendation exists before the relevant transition, not how it's generated.
- Access-change execution — Task 038 (`access_review.py`), which this state machine's later transitions call into but doesn't implement directly.

## Implementation notes

- Read `docs/HANDOVER.md` closely before finalizing state names/transitions — this task should implement its documented contract, not invent a parallel one.
- `docs/AI.md`'s human-in-the-loop principle ('AI recommends → system validates → authorized human approves → backend executes → audit records') is directly enforced by this state machine's transition rules, particularly around the approval and access-transfer states.

## Acceptance criteria

- [ ] Every state and transition from `docs/HANDOVER.md` is implemented and enforced.
- [ ] An invalid/out-of-order transition is rejected with a typed error.
- [ ] Every transition produces a correctly-formed audit event via Task 015.
- [ ] A sensitive transition (e.g. access transfer) cannot proceed without the required prior approval state.

## Tests

- [ ] Unit — valid and invalid transition sequences against the state machine's rules
- [ ] Integration — a full handover lifecycle run against a real database, confirming audit events are recorded at each step
- [ ] Security — confirm no transition sequence can reach 'ownership/access transferred' without passing through required approval — this is the test that matters most here
- [ ] E2E — deferred to Task 034

## Documentation updates

`docs/HANDOVER.md` — update if implementation needed to refine an ambiguous state/transition from the current spec.

## Known limitations

_Fill in at completion._
