# Task 008 — initial migration

**Status:** backlog
**Priority:** P0
**Depends on:** Task 007 (ORM models)
**Requirements:** `docs/DATABASE.md` §9 (every schema change requires a migration)
**Board ref:** `tasks/BOARD.md` — Phase 2.2
**Owner:** Sanmati

## Goal

An Alembic migration that creates the full schema from Task 007's models, and a working `upgrade`/`downgrade` cycle, so the team has one repeatable way to stand up or evolve the database — never manual schema edits.

## Scope

- `migrations/0001_initial_schema.py` (plus whatever Alembic scaffolding it needs — `alembic.ini`, `migrations/env.py`, etc., placed per `docs/IMPLEMENTATION_STRUCTURE.md`).
- Generated from Task 007's models, covering every table in `docs/DATABASE.md` §2.
- A working `downgrade()` that cleanly reverses the migration — not a stub that raises `NotImplementedError`.
- Wired so it runs against the Task 003 compose Postgres instance with a single documented command.

## Out of scope

- Any seed/fixture data — that's a separate concern for local dev convenience, not part of the schema migration itself. If you want dev seed data, note it as a follow-up rather than folding it into this migration.
- RLS policy migrations — deferred with Task 007 until Phase 3's authorization model exists to inform them.

## Implementation notes

- `docs/DATABASE.md` §9 is explicit: "Never modify production-like schema manually as the normal workflow." This migration is the pattern every future schema change follows — get the tooling right once here (naming convention, autogenerate vs. hand-written, how migrations are numbered) rather than everyone improvising differently later.
- Confirm the migration is idempotent to run against a clean database — a fresh `docker compose up` (Task 003) followed by this migration should be the standard "new environment" path, and should be documented as such.

## Acceptance criteria

- [ ] `alembic upgrade head` (or equivalent) creates every table from Task 007 against a clean Task-003 Postgres instance.
- [ ] `alembic downgrade base` (or equivalent) cleanly drops everything it created, with no leftover objects.
- [ ] Running upgrade twice in a row doesn't error or duplicate anything.
- [ ] The exact commands to run this are documented (see below) — not just "it works if you know the incantation."

## Tests

- [ ] Unit — n/a
- [ ] Integration — upgrade/downgrade cycle runs cleanly against a fresh Postgres instance from Task 003
- [ ] Security — n/a beyond what Task 007 already covers
- [ ] E2E — n/a yet

## Documentation updates

- `docs/OPERATIONS.md` — add the exact migration commands (how to run, how to create a new migration, how to reset a local DB) so this isn't tribal knowledge.

## Known limitations

_Fill in at completion._
