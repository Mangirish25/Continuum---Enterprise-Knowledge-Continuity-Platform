# Task 007 — ORM models

**Status:** backlog
**Priority:** P0
**Depends on:** Task 005 (`core/config.py` — needs a database URL to connect against), Task 003 (compose stack — needs a Postgres instance to develop/test against)
**Requirements:** REQ-P002 (track users, projects, assets, ownership, continuity metadata), `docs/DATABASE.md` §2–§8
**Board ref:** `tasks/BOARD.md` — Phase 2.1
**Owner:** Sanmati

## Goal

The SQLAlchemy ORM models for the core entities in `docs/DATABASE.md` §2, matching its tenant, constraint, and audit rules exactly — this is the schema everything else in the backend is built on top of.

## Scope

- `apps/api/app/repositories/models/*.py` (one file per logical group is fine — e.g. `org.py`, `user.py`, `project.py`, `asset.py`, `knowledge.py`, `handover.py`, `risk.py`, `audit.py` — follow whatever grouping `docs/IMPLEMENTATION_STRUCTURE.md` implies, or a sensible one if it doesn't say).
- Every table listed in `docs/DATABASE.md` §2: `organizations`, `departments`, `teams`, `users`, `roles`, `user_roles`, `skills`, `user_skills`, `projects`, `project_members`, `project_dependencies`, `assets`, `knowledge_documents`, `knowledge_chunks`, `integrations`, `external_objects`, `sync_runs`, `handovers`, `handover_tasks`, `handover_approvals`, `ownership_transfers`, `access_actions`, `risk_assessments`, `notifications`, `audit_events`, `audit_verifications`.
- Every tenant-owned table carries `organization_id` directly or through a guaranteed organization-scoped relationship (`docs/DATABASE.md` §3) — this is not optional per-table; verify it for each one.
- `audit_events` matches the exact field list in `docs/DATABASE.md` §8 (`event_id`, `sequence`, `organization_id`, `timestamp`, `actor_type`, `actor_id`, `action_type`, `entity_type`, `entity_id`, `old_state_hash`, `new_state_hash`, `request_id`, `correlation_id`, `metadata`, `previous_hash`, `current_hash`) — do not rename or drop any of these fields; the hash chain (Task 5.x, `audit/ledger.py`) depends on this exact shape.
- `knowledge_documents`/`knowledge_chunks` preserve the metadata list in `docs/DATABASE.md` §6 (source_type, source_url, source_version, checksum, classification, owner_id, ACL fields, parser/chunking/embedding version, timestamps) even though nothing writes to these tables yet (Phase 8) — the schema should exist now so Phase 7–8 don't need a migration just to add fields that were foreseeable from the start.
- External identity fields per §4 (internal user ID as primary key, external provider IDs preserved separately) and external-object uniqueness per §5 (unique per integration + external identifier/version).
- Standard constraints per §7: foreign keys, unique constraints, check constraints, indexes, explicit nullability, deletion policy (soft-delete vs. hard-delete decided per table, documented in the model file as a comment where non-obvious).

## Out of scope

- Alembic migration generation — that's Task 008, which depends on this task.
- Row-Level Security (RLS) policies — `docs/DATABASE.md` §3 says RLS is used "where appropriate," and `docs/SECURITY.md` lists it as one of six authorization layers, but wiring it up is a separate, later concern once the app-layer authorization (Phase 3) exists to compare against. Note in "Known limitations" which tables would benefit from RLS.
- Any actual query/repository logic beyond the model definitions themselves — that starts in Phase 4 (`repositories/project_repository.py`, etc.).

## Implementation notes

- This is the single highest-leverage file in the whole backend — nearly every later task depends on it being right. Prefer being conservative and matching `docs/DATABASE.md` literally over improvising a "cleaner" schema; if you think the documented schema is wrong, flag it rather than silently deviating (`AGENTS.md` §8, change control).
- `current_hash = SHA256(previous_hash || canonical_event)` (§8) is computed by application code (Task 5.x), not the database — this model just needs to store the resulting hashes, not compute them.
- Coordinate naming with Task 009 (`core/security.py`) on how `users`/`roles`/`user_roles` map to JWT claims, so Phase 3 doesn't need to reshape this table.

## Acceptance criteria

- [ ] Every table in `docs/DATABASE.md` §2 has a corresponding model.
- [ ] Every tenant-owned model has `organization_id` or an equivalent guaranteed scoped relationship.
- [ ] `audit_events` model matches the §8 field list exactly.
- [ ] `knowledge_documents`/`knowledge_chunks` include the §6 metadata fields.
- [ ] Foreign keys, unique constraints, and indexes exist for the relationships implied by `docs/DATABASE.md` and the Guide's data model.
- [ ] Models import and instantiate cleanly against a Task-003 Postgres instance (no migration needed yet to prove this — a `create_all` smoke test is enough for this task).

## Tests

- [ ] Unit — models define expected columns, types, nullability, and constraints
- [ ] Integration — models can be created against a real Postgres instance from Task 003 with no errors
- [ ] Security — spot-check that every tenant-owned table actually enforces the `organization_id` rule (this is the check most likely to be skipped under time pressure — don't skip it)
- [ ] E2E — n/a yet

## Documentation updates

- If any table's shape had to deviate from `docs/DATABASE.md` for a concrete technical reason, update `docs/DATABASE.md` to match and explain why — don't let code and doc silently diverge.

## Known limitations

_Fill in at completion — e.g. which tables would benefit from RLS once Phase 3 lands._
