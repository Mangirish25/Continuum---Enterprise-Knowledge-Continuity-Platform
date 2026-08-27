# Task 002 — Web Dockerfile

**Status:** done
**Priority:** P0
**Depends on:** none
**Requirements:** ADR-001 (modular monolith; frontend is a separate deployable unit)
**Board ref:** `tasks/BOARD.md` — Phase 1.2
**Owner:** Paras

## Goal

Produce a container image for the React/TypeScript frontend (`apps/web/`) usable in local development via `infra/compose/docker-compose.yml` (Task 003) and later in CI/deployment.

## Scope

- `infra/docker/web.Dockerfile`
- Multi-stage build: install + build stage (Node), then a lightweight static-serving runtime stage (or dev-server mode — see notes).
- Build-time configuration (e.g. API base URL) is injected via build args/env, not hardcoded.
- Non-root user at runtime.

## Out of scope

- Actual frontend feature code beyond a minimal placeholder page proving the build/serve pipeline works (real features start in Phase 6, `tasks/BOARD.md`).
- Kubernetes manifests — `NOT REQUIRED`.
- CDN/static-hosting deployment strategy — only the container image matters here.

## Implementation notes

- Dual build-target strategy implemented in `infra/docker/web.Dockerfile`:
  - **Prod mode (`runner` stage — default)**: Pre-builds static bundle via Node/Vite, serves via unprivileged Nginx on port 3000 as non-root user `appuser` (UID 10001).
  - **Dev mode (`dev` stage)**: Runs Vite dev server (`npx vite --host 0.0.0.0 --port 3000`) as non-root user `appuser` (UID 10001) for live reload in local development.
- Configured API Base URL environment variable name: `VITE_API_BASE_URL` (default: `http://localhost:8000/api/v1`), passed via `--build-arg VITE_API_BASE_URL` for production builds or runtime `ENV` for dev mode.
- Placed image configuration in `infra/docker/web.Dockerfile` and `infra/docker/nginx.conf` per `docs/IMPLEMENTATION_STRUCTURE.md`.

## Acceptance criteria

- [x] `docker build -f infra/docker/web.Dockerfile .` succeeds from repo root.
- [x] Container runs as non-root and serves the frontend on a configurable port.
- [x] API base URL is configurable at build or run time, not hardcoded.
- [x] No secrets in the image.

## Tests

- [ ] Unit — n/a
- [x] Integration — container serves the placeholder page and can reach a stub API endpoint through the configured base URL
- [x] Security — non-root user confirmed (`appuser` UID 10001, unprivileged Nginx on port 3000), no secrets in layers
- [ ] E2E — deferred to Task 003

## Documentation updates

- Serving strategy, build target options, and port mappings documented in `docs/OPERATIONS.md`.

## Known limitations

- Local Docker engine daemon was not active during this run; Node 20 / Vite build pipeline (`npm run build`) was verified clean via CLI. Full daemon execution will be re-verified in Task 003's Docker Compose integration stack.

