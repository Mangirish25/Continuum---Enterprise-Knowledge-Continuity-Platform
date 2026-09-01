# Task 016 — `apps/api/app/audit/verification.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 015 (audit ledger — verification reads what it writes and must use the identical canonicalization/hashing logic)
**Requirements:** REQ-S006 (make audit modifications detectable), ADR-007, `docs/SECURITY.md` §Audit ("verification endpoint")
**Board ref:** `tasks/BOARD.md` — Phase 5.2
**Owner:** Sanmati

## Goal

A way to prove the audit chain hasn't been tampered with — walk the chain, recompute each hash, and report exactly where it breaks if it does. This is what makes ADR-007's "tamper-evident" claim actually true rather than aspirational.

## Scope

- `apps/api/app/audit/verification.py`
- A verification routine that walks `audit_events` in sequence order, recomputes `current_hash = SHA256(previous_hash || canonical_event)` for each event using Task 015's exact canonicalization logic (import/reuse it — do not reimplement it separately, or the two will drift and verification will be meaningless), and confirms it matches the stored `current_hash`, and that each event's `previous_hash` matches the prior event's `current_hash`.
- On success: a clear "chain verified, N events, no discrepancies" result.
- On failure: identify the exact event where the chain breaks (by `event_id`/`sequence`) rather than just reporting "verification failed" — an unusable failure report defeats the purpose of tamper-evidence.
- Writes its own result to `audit_verifications` (Task 007's model) — a verification run is itself a recorded, auditable event.
- A callable entry point suitable for both a scheduled/periodic job and an on-demand API/CLI trigger (`docs/SECURITY.md` §Audit explicitly calls for a "verification endpoint" — expose this as something Task 013-style route or an internal script can call; a full HTTP route can be a thin wrapper added later if not built in this task, but the underlying verification function must be ready to be called that way).

## Out of scope

- The HTTP endpoint itself, if not built directly in this task — this task's core deliverable is the verification *logic*; whether it's exposed via a dedicated route or a script is a smaller follow-up either way.
- External immutable checkpoint verification — deferred with Task 015, per ADR-007's "may use an external immutable checkpoint" being optional stronger protection, not required now.
- Automatic remediation of a broken chain — this task detects and reports; deciding what to do about a real tamper event (freeze the system? alert? both?) is an operational/incident-response decision, not something to hardcode here. Note it as a follow-up.

## Implementation notes

- The whole point of this task is catching real tampering — write a test that actually corrupts a row in a test database (change one field after the fact) and confirms verification correctly flags it at the right event, not just that verification passes on an untouched chain. A verification routine that's only ever tested against clean data hasn't actually been proven to work.
- Reuse, don't reimplement, Task 015's hashing/canonicalization. If you find yourself writing a second version of that logic here, stop — refactor Task 015 to expose a shared function instead.

## Acceptance criteria

- [ ] Verification correctly passes on an untampered chain.
- [ ] Verification correctly detects and precisely identifies the break point when a row is tampered with in a test database.
- [ ] Verification correctly detects a broken `previous_hash`/`current_hash` link even if individual rows' fields weren't touched (i.e. catches reordering/deletion, not just field edits).
- [ ] A verification run itself is recorded (in `audit_verifications`).
- [ ] The verification function is callable both as a scheduled/periodic job and on demand.

## Tests

- [ ] Unit — hash/link verification logic against known-good and known-corrupted synthetic chains
- [ ] Integration — full verification run against a real Postgres instance seeded by Task 015
- [ ] Security — the tamper-detection test (deliberately corrupt a row, confirm it's caught and correctly located) is mandatory, not optional
- [ ] E2E — n/a beyond the integration test above

## Documentation updates

- `docs/OPERATIONS.md` — document how to trigger a verification run (schedule and/or on-demand) and what a failure means operationally.

## Known limitations

_Fill in at completion — note whether an HTTP-exposed verification endpoint was built or only the underlying callable, and whether remediation/alerting on failure is wired up or left as a follow-up._
