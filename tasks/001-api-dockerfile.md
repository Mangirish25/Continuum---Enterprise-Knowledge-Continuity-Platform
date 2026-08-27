# Task 001 — API Dockerfile

**Status:** completed
**Priority:** P0
**Depends on:** none
**Requirements:** REQ-R001 (async/deployable backend), ADR-001 (modular monolith)
**Board ref:** `tasks/BOARD.md` — Phase 1.1
**Owner:** Paras

## Goal

Produce a container image for the FastAPI backend (`apps/api/`) that runs locally via `infra/compose/docker-compose.yml` (Task 003) and is the same image used in CI (Task 008) and, later, deployment.

## Scope

- `infra/docker/api.Dockerfile`
- Multi-stage build: a build stage that installs dependencies, a slim runtime stage that copies only what's needed to run.
- Runs the FastAPI app via an ASGI server (e.g. `uvicorn`) with a configurable host/port.
- Non-root user at runtime.
- Reads configuration from environment variables only (see Task 005 — `core/config.py`); the image itself contains no secrets and no `.env` file.
- Health-check-friendly: the app should expose a way to verify it's serving (an endpoint is fine to leave as a stub for now — a real `/health` route is out of scope here, see Task 010+).

## Out of scope

- Actual application code inside `apps/api/app/` beyond whatever minimal stub is needed to prove the image runs (that's later phases).
- Kubernetes manifests — explicitly `NOT REQUIRED` per `docs/DECISIONS.md`.
- Production secret injection mechanism — only the *pattern* (env vars in, no baked-in secrets) matters here; the actual production secret store is out of scope for this task.

## Implementation notes

- Follow `docs/IMPLEMENTATION_STRUCTURE.md` for where the Dockerfile lives (`infra/docker/`).
- Keep the image small — this affects rebuild speed during vibe coding and CI iteration time, not just production.
- Do not add OS packages "just in case" — every added package should be traceable to something the app actually needs (`AGENTS.md` §6: "Do not add a dependency without explaining its purpose and impact" applies to image layers too).
- Coordinate with Task 005 (`core/config.py`) on which env var names the app expects, so the Dockerfile's documented/example env vars match Task 004's `.env.example`.

## Acceptance criteria

- [x] `docker build -f infra/docker/api.Dockerfile .` succeeds from repo root.
- [x] Resulting container runs as a non-root user (`USER appuser`, UID/GID 10001).
- [x] Container starts and serves on a configurable port without requiring a baked-in `.env` file (`APP_HOST`, `APP_PORT`, `LOG_LEVEL` env vars).
- [x] No secret values, tokens, or credentials appear anywhere in the Dockerfile or image layers.
- [x] Image size and build time are reasonable for local iterative use (multi-stage build from `python:3.11-slim`).

## Tests

- [ ] Unit — n/a (infra artifact)
- [x] Integration — container boots, health probe turns healthy, and responds `200 OK` on `/health` endpoint.
- [x] Security — confirmed non-root user (`appuser`), confirmed no secrets in image.
- [ ] E2E — deferred to Task 003 (compose brings this up alongside Postgres/Redis/MinIO)

## Documentation updates

- None required (matches standard build/run patterns in `docs/OPERATIONS.md`).

## Known limitations

- The application inside `apps/api/app/main.py` is a minimal FastAPI stub providing `/health` for Task 001 verification; domain logic will be expanded in Phase 2+.


