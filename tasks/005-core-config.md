# Task 005 — `apps/api/app/core/config.py`

**Status:** done
**Priority:** P0
**Depends on:** Task 004 (`.env.example`, so the variable names are agreed)
**Requirements:** REQ-S004 (protect secrets), supports REQ-R001 (async/deployable backend)
**Board ref:** `tasks/BOARD.md` — Phase 1.5
**Owner:** Sanmati

## Goal

A single, typed settings object the rest of the backend imports for all configuration — no module reads `os.environ` directly outside this file.

## Scope

- `apps/api/app/core/config.py`
- A typed settings class (e.g. Pydantic `BaseSettings`) loading from environment variables, with `.env` support for local dev only.
- Covers at minimum: database URL, Redis URL, object storage endpoint/credentials, app environment (`dev`/`viva`/`prod` — see `docs/DECISIONS.md` ADR-014 on dev-vs-viva mode), JWT signing config placeholder (real implementation in Task 3.1), and a placeholder section for the LLM provider keys that Task 8.x will need (`GEMINI_API_KEY_1`/`GEMINI_API_KEY_2`, `GROQ_API_KEY`) so later tasks extend this file rather than fighting it.
- Fails fast and loudly on startup if a required variable is missing in non-dev environments — do not silently default a required production value.

## Out of scope

- Actual secret *storage* mechanism for production (`docs/SECURITY.md` — separate concern).
- Any business logic — this is configuration loading only.

## Implementation notes

- Created `apps/api/app/core/config.py` with `Settings` (inheriting from `pydantic_settings.BaseSettings`) and typed `ConfigurationError`.
- Matches variable names from `infra/secrets/.env.example` exactly.
- Enforces fail-fast startup checks when `APP_MODE` is `viva` or `prod` (preventing fallback to insecure default JWT secrets or database/MinIO passwords).
- Unit tested in `apps/api/tests/test_config.py` (5 passed).

## Acceptance criteria

- [x] All config values used by any other Phase-1 task are read through this module, not ad hoc `os.environ` calls.
- [x] Missing required variables cause a clear, typed startup error (not a raw `KeyError`/traceback) — see `AGENTS.md` §3 "typed error base classes" (Task 006).
- [x] Local dev works from `.env` (Task 004) with zero code changes.
- [x] No default value for anything security-sensitive (e.g. no hardcoded fallback JWT secret) in non-dev mode.

## Tests

- [x] Unit — settings load correctly from env vars; missing required var raises the expected typed error (`ConfigurationError`); dev-mode defaults behave as documented (`apps/api/tests/test_config.py`)
- [ ] Integration — n/a yet
- [x] Security — confirmed no secret-sensitive setting has an unsafe default outside dev mode
- [ ] E2E — n/a

## Documentation updates

- None required — settings shape matches `infra/secrets/.env.example` and `docs/OPERATIONS.md`.

## Known limitations

- Task 006 will establish generic `EKCPError` base classes in `apps/api/app/core/exceptions.py`. `ConfigurationError` is currently defined in `apps/api/app/core/config.py` and can inherit from `EKCPError` once Task 006 lands.

