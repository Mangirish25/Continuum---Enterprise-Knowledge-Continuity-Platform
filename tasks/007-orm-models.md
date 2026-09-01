# Task 007 — ORM models

**Status:** done
**Priority:** P0
**Depends on:** Task 005 (`core/config.py` — needs a database URL to connect against), Task 003 (compose stack — needs a Postgres instance to develop/test against)
**Requirements:** REQ-P002 (track users, projects, assets, ownership, continuity metadata), `docs/DATABASE.md` §2–§8
**Board ref:** `tasks/BOARD.md` — Phase 2.1
**Owner:** Sanmati

## Goal

The SQLAlchemy ORM models for the core entities in `docs/DATABASE.md` §2, matching its tenant, constraint, and audit rules exactly — this is the schema everything else in the backend is built on top of.

## Scope

- `apps/api/app/repositories/models/*.py` (one file per logical group: `base.py`, `org.py`, `user.py`, `project.py`, `asset.py`, `knowledge.py`, `integration.py`, `handover.py`, `risk.py`, `notification.py`, `audit.py`).
- Every table listed in `docs/DATABASE.md` §2: `organizations`, `departments`, `teams`, `users`, `roles`, `user_roles`, `skills`, `user_skills`, `projects`, `project_members`, `project_dependencies`, `assets`, `knowledge_documents`, `knowledge_chunks`, `integrations`, `external_objects`, `sync_runs`, `handovers`, `handover_tasks`, `handover_approvals`, `ownership_transfers`, `access_actions`, `risk_assessments`, `notifications`, `audit_events`, `audit_verifications`.
- Every tenant-owned table carries `organization_id` directly or through a guaranteed organization-scoped relationship (`docs/DATABASE.md` §3).
- `audit_events` matches the exact field list in `docs/DATABASE.md` §8 (`event_id`, `sequence`, `organization_id`, `timestamp`, `actor_type`, `actor_id`, `action_type`, `entity_type`, `entity_id`, `old_state_hash`, `new_state_hash`, `request_id`, `correlation_id`, `metadata`, `previous_hash`, `current_hash`).
- `knowledge_documents`/`knowledge_chunks` preserve the metadata list in `docs/DATABASE.md` §6 (source_type, source_url, source_version, checksum, classification, owner_id, ACL fields, parser/chunking/embedding version, timestamps).
- External identity fields per §4 and external-object uniqueness per §5.
- Standard constraints per §7: foreign keys, unique constraints, check constraints, indexes, explicit nullability.

## Out of scope

- Alembic migration generation — that's Task 008, which depends on this task.
- Row-Level Security (RLS) policies — `docs/DATABASE.md` §3 says RLS is used "where appropriate," and `docs/SECURITY.md` lists it as one of six authorization layers, but wiring it up is a separate, later concern once the app-layer authorization (Phase 3) exists to compare against. Note in "Known limitations" which tables would benefit from RLS.
- Any actual query/repository logic beyond the model definitions themselves — that starts in Phase 4 (`repositories/project_repository.py`, etc.).

## Implementation notes

- Implemented database session factory in `apps/api/app/core/database.py`.
- Implemented `DeclarativeBase` base model in `apps/api/app/repositories/models/base.py`.
- Created all 26 ORM models across 10 modular files in `apps/api/app/repositories/models/`.
- Exported all 26 models in `apps/api/app/repositories/models/__init__.py`.
- Tested in `apps/api/tests/test_models.py` (6 passed, 15 total backend tests passing).

## Acceptance criteria

- [x] Every table in `docs/DATABASE.md` §2 has a corresponding model.
- [x] Every tenant-owned model has `organization_id` or an equivalent guaranteed scoped relationship.
- [x] `audit_events` model matches the §8 field list exactly.
- [x] `knowledge_documents`/`knowledge_chunks` include the §6 metadata fields.
- [x] Foreign keys, unique constraints, and indexes exist for the relationships implied by `docs/DATABASE.md` and the Guide's data model.
- [x] Models import and instantiate cleanly against a Task-003 Postgres instance (no migration needed yet to prove this — a `create_all` smoke test is enough for this task).

## Tests

- [x] Unit — models define expected columns, types, nullability, and constraints (`apps/api/tests/test_models.py`)
- [x] Integration — models can be created against a real database / create_all engine with no errors (`apps/api/tests/test_models.py`)
- [x] Security — spot-check that every tenant-owned table actually enforces the `organization_id` rule (`apps/api/tests/test_models.py`)
- [ ] E2E — n/a yet

## Documentation updates

- None required — model definitions strictly match `docs/DATABASE.md` §2–§8 without deviation.

## Known limitations

- PostgreSQL Row-Level Security (RLS) policies are deferred per scope until Phase 3 authorization policies exist. Tables that would benefit most from RLS once Phase 3 lands: `organizations`, `projects`, `assets`, `knowledge_documents`, `knowledge_chunks`, `handovers`, `audit_events`.

