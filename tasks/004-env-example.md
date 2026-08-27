# Task 004 — `.env.example`

**Status:** done
**Priority:** P0
**Depends on:** none (should land alongside/before Task 003, so compose has something to reference)
**Requirements:** REQ-S004 (protect secrets and external credentials)
**Board ref:** `tasks/BOARD.md` — Phase 1.4
**Owner:** Paras

## Goal

A single documented, committed `.env.example` that lists every environment variable the local stack needs — with placeholder or safe-default values only — so no one has to reverse-engineer required config from code.

## Scope

- `infra/secrets/.env.example`
- Every variable referenced by Task 001–003 (Postgres connection, Redis URL, MinIO/S3 credentials and endpoint, API port, web API base URL) with a one-line comment explaining what it's for.
- A short header comment: "Copy this to `.env` at the repo root (or wherever `docker-compose.yml` expects it) and fill in real values. Never commit `.env`."
- Placeholder rows for values that will exist later but aren't needed yet (e.g. `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2` — see `docs/DECISIONS.md` ADR-011 on the two-key demo-day safety net) so the file doesn't need repeated restructuring as later phases land — but leave them clearly marked `# not yet used — Phase 8` rather than pretending they're active.

## Out of scope

- The actual production secret-management mechanism (`docs/SECURITY.md` §Secrets says production uses a proper secret store — this task is dev-only).
- Real credential values of any kind, anywhere in this file or its git history.

## Implementation notes

- Created `infra/secrets/.env.example` with standard safe defaults for Postgres, Redis, MinIO, API, and Web.
- Created root `.gitignore` verifying `.env` is ignored and `.env.example` is tracked.
- Included commented placeholders for Phase 3 (`JWT_SECRET_KEY`) and Phase 8 (`GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`, `GROQ_API_KEY`).
- Documented developer setup workflow in `docs/OPERATIONS.md`.

## Acceptance criteria

- [x] `.env.example` exists at `infra/secrets/.env.example` and lists every variable currently required by Tasks 001–003.
- [x] `.env` is confirmed present in `.gitignore`.
- [x] Every variable has an explanatory comment.
- [x] No real credentials anywhere in the file.
- [x] Copying this file to `.env` and filling in local values is sufficient to run Task 003's compose stack.

## Tests

- [ ] Unit — n/a
- [x] Integration — verified `.env.example` variables align with `infra/compose/docker-compose.yml`, `api.Dockerfile`, and `web.Dockerfile`
- [x] Security — confirmed `.env` is present in `.gitignore`; no real API keys or credentials in `.env.example`
- [ ] E2E — n/a

## Documentation updates

- `docs/OPERATIONS.md` — referenced `infra/secrets/.env.example` as the initial step for developer setup.

## Known limitations

- Task 005 (`apps/api/app/core/config.py`) will implement Pydantic BaseSettings loading; variable names match Task 005 requirements, but validation logic will be enforced in Task 005.
