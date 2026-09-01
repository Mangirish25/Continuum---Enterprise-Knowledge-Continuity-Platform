# Task 008 — initial migration

**Status:** done
**Priority:** P0
**Depends on:** Task 007 (ORM models)
**Requirements:** `docs/DATABASE.md` §9 (every schema change requires a migration)
**Board ref:** `tasks/BOARD.md` — Phase 2.2
**Owner:** Sanmati

## Goal

An Alembic migration that creates the full schema from Task 007's models, and a working `upgrade`/`downgrade` cycle, so the team has one repeatable way to stand up or evolve the database — never manual schema edits.

## Scope

- `migrations/versions/0001_initial_schema.py` and `migrations/0001_initial_schema.py` (plus Alembic scaffolding — `alembic.ini`, `migrations/env.py`, `migrations/script.py.mako`).
- Generated from Task 007's models, covering every table in `docs/DATABASE.md` §2.
- A working `downgrade()` that cleanly reverses the migration — dropping all 26 tables in reverse dependency order.
- Wired so it runs against the Task 003 compose Postgres instance or local databases with `alembic upgrade head`.

## Out of scope

- Any seed/fixture data — separate concern for local dev convenience.
- RLS policy migrations — deferred with Task 007 until Phase 3's authorization model exists.

## Implementation notes

- Created Alembic configuration in `alembic.ini` and environment setup in `migrations/env.py`.
- Created initial migration script in `migrations/versions/0001_initial_schema.py` covering all 26 tables, foreign keys, indexes, and unique constraints.
- Created programmatic integration test in `apps/api/tests/test_migrations.py` verifying full `upgrade('head')` -> `downgrade('base')` -> `upgrade('head')` cycle.
- Documented migration CLI workflow in `docs/OPERATIONS.md`.

## Acceptance criteria

- [x] `alembic upgrade head` creates every table from Task 007 against a clean database instance.
- [x] `alembic downgrade base` cleanly drops everything it created, with no leftover objects.
- [x] Running upgrade twice in a row doesn't error or duplicate anything.
- [x] The exact commands to run this are documented in `docs/OPERATIONS.md`.

## Tests

- [ ] Unit — n/a
- [x] Integration — upgrade/downgrade cycle runs cleanly in `apps/api/tests/test_migrations.py` (16 total backend tests passing)
- [ ] Security — n/a beyond what Task 007 already covers
- [ ] E2E — n/a yet

## Documentation updates

- `docs/OPERATIONS.md` — added exact migration commands for running pending migrations, rolling back, autogenerating new revisions, and resetting development databases.

## Known limitations

- PostgreSQL-specific features like Row-Level Security (RLS) policies or custom extensions (e.g. pgvector for Phase 8) are deferred to future targeted migrations.

