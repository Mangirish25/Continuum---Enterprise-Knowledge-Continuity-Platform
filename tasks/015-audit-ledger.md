# Task 015 — `apps/api/app/audit/ledger.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 007 (ORM models — needs the exact `audit_events` shape from `docs/DATABASE.md` §8), Task 008 (initial migration)
**Requirements:** REQ-P008 (record important actions in a tamper-evident audit ledger), REQ-S006 (make audit modifications detectable), ADR-007 (tamper-evident audit ledger)
**Board ref:** `tasks/BOARD.md` — Phase 5.1
**Owner:** Sanmati

## Goal

The single writer through which every important state change in the system produces a chained, tamper-evident audit event — implementing ADR-007 exactly as specified: "a relational audit event model with canonical cryptographic chaining and controlled concurrent writes."

## Scope

- `apps/api/app/audit/ledger.py`
- A `record_event(...)` (or equivalent) function/service that:
  1. builds an event from the caller's data (`actor_type`, `actor_id`, `action_type`, `entity_type`, `entity_id`, `old_state_hash`, `new_state_hash`, `request_id`, `correlation_id`, `metadata`),
  2. fetches the current chain tail (`previous_hash`) for the relevant scope,
  3. computes `current_hash = SHA256(previous_hash || canonical_event)` exactly as specified in `docs/DATABASE.md` §8 — canonicalization (e.g. a deterministic JSON serialization) must be defined precisely and documented, since any ambiguity here breaks verification later,
  4. writes the event to `audit_events` (Task 007's model) as an append-only insert — this module must never update or delete an existing `audit_events` row.
- Serialized/controlled concurrent writes so two simultaneous writers cannot produce conflicting predecessors (`docs/DATABASE.md` §8 — this is not optional; a race here silently breaks the whole chain's integrity guarantee). Use a database-level mechanism (e.g. row locking, a serializable transaction, or an equivalent) rather than an in-process lock, since the API may run multiple instances/workers.
- A clear internal API other modules call rather than writing to `audit_events` directly — no module should ever `INSERT INTO audit_events` on its own; everything routes through this file.

## Out of scope

- Chain verification logic — that's Task 016, which reads what this task writes.
- External immutable/WORM checkpointing — ADR-007 mentions this as an optional *stronger* protection layer, not required now. Note it as a future option in "Known limitations" rather than building it.
- Deciding *which* actions across the codebase call this (e.g. wiring it into Task 013/014's endpoints) — that's the responsibility of each task that performs a sensitive action; this task only builds the ledger itself. If you want to prove it end-to-end, a minimal test call is fine, but broad call-site integration is future work.

## Implementation notes

- This is one of the most architecturally sensitive files in the codebase — get the canonicalization and hashing exactly right and document it precisely, because Task 016's verification and any future external audit depend on being able to reproduce the same hash deterministically from the same inputs.
- `docs/SECURITY.md` §Audit lists "controlled writer permissions" — consider whether this module should be the *only* code path with `INSERT` permission on `audit_events` at the database level, not just by convention. If that's not feasible yet, note it as a known gap rather than silently skipping the control.
- Concurrency correctness matters more than raw throughput here — a lost or misordered event breaks the chain for everything after it.

## Acceptance criteria

- [ ] `record_event(...)` correctly computes `current_hash = SHA256(previous_hash || canonical_event)` and persists a new, correctly-chained row.
- [ ] Canonicalization of the event for hashing is deterministic and documented (same logical event always hashes the same way).
- [ ] Concurrent calls to `record_event` from multiple simultaneous writers never produce two events with the same `previous_hash` (i.e. no forked chain) — this must be tested under actual concurrency, not just reasoned about.
- [ ] No code path in this module updates or deletes an existing `audit_events` row.
- [ ] The module exposes a clear, documented API that other tasks can call without needing to understand the hashing internals.

## Tests

- [ ] Unit — hash computation is correct and deterministic for known inputs; canonicalization handles edge cases (unicode, nested metadata, key ordering) consistently
- [ ] Integration — sequential writes produce a valid, verifiable chain against a real Postgres instance
- [ ] Concurrency — simultaneous writes (e.g. from multiple async tasks/processes) never produce a forked or corrupted chain; this is the single most important test in this task
- [ ] Security — confirm append-only behavior (no update/delete path exists); confirm a tampered row would in fact break verification (this can be a shared test with Task 016 once it exists)

## Documentation updates

- `docs/DATABASE.md` — if the canonicalization scheme needs to be specified precisely (it currently isn't, beyond "canonical_event"), add that detail here so it's not only defined in code comments.

## Known limitations

_Fill in at completion — explicitly note whether database-level write restriction on `audit_events` was implemented or deferred, and whether external checkpointing remains a future option._
