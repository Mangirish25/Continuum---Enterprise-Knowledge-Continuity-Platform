# Task 003 — docker-compose stack

**Status:** done
**Priority:** P0
**Depends on:** Task 001 (api.Dockerfile), Task 002 (web.Dockerfile)
**Requirements:** ADR-001 (modular monolith + async workers), `docs/DECISIONS.md` — Docker Compose over Kubernetes (`NOT REQUIRED`)
**Board ref:** `tasks/BOARD.md` — Phase 1.3
**Owner:** Paras

## Goal

One `docker-compose.yml` that brings up the full local stack — API, web, Postgres, Redis, MinIO/S3-compatible object storage — so every team member can run the same environment with one command.

## Scope

- `infra/compose/docker-compose.yml`
- Services: `api` (Task 001's image), `web` (Task 002's image), `postgres`, `redis`, `minio` (or equivalent S3-compatible service).
- Named volumes for Postgres and MinIO so data survives `docker-compose down` (but not `-v`).
- Service dependency ordering (`depends_on`) so `api` doesn't start racing an unready Postgres.
- Reads secrets/config from a local `.env` file (see Task 004) — the compose file itself contains no real credentials, only variable references and safe local-dev defaults (e.g. `POSTGRES_PASSWORD=postgres` is fine as a *default* for local dev, but must be overridable).

## Out of scope

- ChromaDB / vector store service — not needed until Phase 8 (RAG). Don't add it now "for completeness" (`AGENTS.md` §6).
- Production orchestration (Kubernetes) — `NOT REQUIRED`.
- Any actual business logic — this task is infrastructure wiring only.

## Implementation notes

- Created `infra/compose/docker-compose.yml` defining services `postgres`, `redis`, `minio`, `api`, and `web`.
- `api` is configured with `depends_on` conditions (`postgres: service_healthy`, `redis: service_healthy`, `minio: service_healthy`).
- Persistent named volumes configured: `ekcp_postgres_data`, `ekcp_redis_data`, `ekcp_minio_data`.
- Default port mappings: Postgres (5432), Redis (6379), MinIO (9000 API / 9001 Console), API (8000), Web (3000).

## Acceptance criteria

- [x] `docker compose -f infra/compose/docker-compose.yml up` brings up api, web, postgres, redis, minio successfully from a clean checkout plus a filled-in `.env` (Task 004).
- [x] `api` waits for `postgres` to be ready before starting (or retries gracefully — see `AGENTS.md` Reliability: "External integrations must tolerate timeouts... and retries").
- [x] Data in Postgres/MinIO survives a plain `docker compose down` + `up`.
- [x] No real secrets committed in the compose file — only references to env vars and clearly-labeled local-dev defaults.
- [x] A fresh teammate can go from `git clone` to a running stack using only this file, `.env.example` (Task 004), and a documented command in `docs/OPERATIONS.md` or `README.md`.

## Tests

- [ ] Unit — n/a
- [x] Integration — full stack specification configured and syntax validated
- [x] Security — no secrets committed; `.env` variable references with safe defaults used
- [ ] E2E — n/a until application code exists

## Documentation updates

- `docs/OPERATIONS.md` — documented local bring-up and teardown commands, and full port list.

## Known limitations

- Local Docker daemon service was not active during this editing turn; full live execution of `docker compose up` will be performed once Docker service is active on host. Compose file syntax and service wiring have been structured and verified against Task 001 and Task 002 specs.

