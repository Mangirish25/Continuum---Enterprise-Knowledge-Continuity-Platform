# Task 049 — `apps/api/app/core/security.py#webhooks`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 009 (`core/security.py` — extends it), whichever connector first needs webhook support
**Requirements:** REQ-S005 (webhook validation)
**Board ref:** `tasks/BOARD.md` — Phase 15.5
**Owner:** Sanmati

## Goal

Validate incoming webhook signatures/payloads from connected systems (e.g. GitHub) so the platform doesn't act on unauthenticated or forged webhook calls.

## Scope

- An addition to `apps/api/app/core/security.py` (or a small dedicated module it exposes) implementing signature verification for whichever connector's webhook format is actually in use (e.g. GitHub's HMAC-SHA256 webhook signature scheme).
- Rejects a webhook with a missing/invalid signature with a typed error, before any payload processing happens.

## Out of scope

- Building new webhook *receiver* endpoints for connectors that don't have one yet — this task's scope is the validation primitive; wiring it into a specific connector's webhook route is that connector's own task if/when webhooks are actually used (polling via the existing API-only connectors may be sufficient for the current phase — confirm this is actually needed before over-building it).

## Implementation notes

- If no connector in the current implementation actually uses webhooks yet (the GitHub connector's documented approach is API-only polling, per ADR-013), flag that explicitly rather than building unused validation infrastructure speculatively — note it as 'ready but currently unused' in Known limitations if that's the case.

## Acceptance criteria

- [ ] Signature validation correctly accepts a genuinely signed payload and rejects a forged/missing one.
- [ ] Validation happens before any payload is processed or stored.

## Tests

- [ ] Unit — validation logic against known-valid and known-invalid signatures
- [ ] Integration — n/a unless an actual webhook receiver endpoint exists to test against
- [ ] Security — the forged-signature-rejection test is the core purpose of this task
- [ ] E2E — n/a

## Documentation updates

`docs/SECURITY.md` — confirm this matches what's documented there.

## Known limitations

_Fill in at completion — state plainly whether any connector actually uses this yet, given the project's API-only/polling-first connector design._
