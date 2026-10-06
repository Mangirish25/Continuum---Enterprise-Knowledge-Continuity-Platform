# Task 038 — `apps/api/app/modules/handover/access_review.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 033 (handover state machine), Task 009 (RBAC), Task 015 (audit ledger)
**Requirements:** REQ-P005 (controlled, human-approved ownership/access transfer), ADR-007
**Board ref:** `tasks/BOARD.md` — Phase 12.1
**Owner:** Sanmati

## Goal

Execute the actual access/ownership changes a handover authorizes — strictly after human approval, per `docs/AI.md`'s human-in-the-loop principle, and fully audited.

## Scope

- `apps/api/app/modules/handover/access_review.py`
- Reads an approved handover's required access changes (ownership transfer, permission revocation/grant) and executes them against `access_actions`/`ownership_transfers` (`docs/DATABASE.md` §2).
- Callable only from a handover state that has already passed through Task 033's required approval transition — this module must verify that precondition itself, not merely trust the caller.
- Every executed change writes an audit event via Task 015.

## Out of scope

- Actually revoking access in external systems (e.g. removing a GitHub repo collaborator) — unless an existing connector already supports write operations, this task's scope is the platform's own internal record of the access change; note any external-system enforcement gap explicitly rather than silently implying it's handled.

## Implementation notes

- This is one of the most sensitive write paths in the system — the precondition check (approval already happened) must be enforced in this module itself, not merely assumed because Task 034's API wouldn't normally call it out of order. Defense in depth matters here specifically because this changes who can access what.

## Acceptance criteria

- [ ] Access changes execute only for handovers that have genuinely passed required approval — verified by this module, not just trusted from the caller.
- [ ] Every executed change is recorded in `access_actions`/`ownership_transfers` and produces a correctly-formed audit event.
- [ ] An attempt to execute an access change for a non-approved handover is rejected with a typed error.

## Tests

- [ ] Unit — precondition enforcement against both approved and non-approved handover states
- [ ] Integration — a full approved-handover-to-executed-access-change flow against a real database
- [ ] Security — the non-approved-rejection test is mandatory — attempt to call this module directly bypassing Task 034's API and confirm it's still rejected
- [ ] E2E — full flow: Task 034 approval → this module executes → Task 016 verification confirms the audit chain is intact

## Documentation updates

`docs/HANDOVER.md` — document which external-system access changes are and aren't actually enforced by this module, if that scope was narrowed.

## Known limitations

_Fill in at completion — be explicit about whether external-system access revocation (e.g. actual GitHub permission removal) is implemented or only internally recorded._
