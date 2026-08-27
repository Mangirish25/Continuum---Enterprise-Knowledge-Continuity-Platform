# Operations

## Development

Use reproducible containers/configuration where practical.

To set up your local developer environment:
1. Copy `infra/secrets/.env.example` to `.env` at the repository root:
   ```bash
   cp infra/secrets/.env.example .env
   ```
2. Fill in local credentials or override default ports if needed. Never commit `.env`.


## Production direction

Production should use:
- managed/secure secret storage,
- structured logs,
- metrics,
- tracing where appropriate,
- backups,
- restore procedure,
- controlled deployment,
- least-privilege service accounts.

## Observability

Every request/job should have a request or correlation ID where practical.

Log structured events with:
- timestamp,
- severity,
- component,
- operation,
- correlation ID,
- safe identifiers,
- error code.

Never log secrets or sensitive document content unnecessarily.

## Backup and recovery

PostgreSQL backups must have a documented restore procedure.

The vector index is derived and should be rebuildable from source content and metadata.

## Deployment

Docker/Compose is sufficient for the initial project deployment. Kubernetes is optional and must not be introduced merely for appearance.

### Web Container Image (`infra/docker/web.Dockerfile`)

The React/TypeScript frontend container supports two multi-stage build targets:

1. **Production Mode (`runner` stage — default)**
   - Serves pre-built static React bundle via unprivileged Nginx on port `3000`.
   - Runs as non-root user `appuser` (UID 10001).
   - Build command: `docker build -f infra/docker/web.Dockerfile --build-arg VITE_API_BASE_URL=http://localhost:8000/api/v1 -t ekcp-web:latest .`

2. **Development Mode (`dev` stage)**
   - Runs Vite dev server (`npx vite --host 0.0.0.0 --port 3000`) for hot-reloading.
   - Build command: `docker build --target dev -f infra/docker/web.Dockerfile -t ekcp-web:dev .`

### Local Infrastructure (`infra/compose/docker-compose.yml`)

Bring up the full local stack (Postgres, Redis, MinIO, API, Web):

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

Teardown (persisting volumes):
```bash
docker compose -f infra/compose/docker-compose.yml down
```

Teardown (deleting volumes):
```bash
docker compose -f infra/compose/docker-compose.yml down -v
```

### Port Mappings
- **Web Frontend**: `3000`
- **FastAPI Backend**: `8000`
- **PostgreSQL**: `5432`
- **Redis**: `6379`
- **MinIO S3 API**: `9000`
- **MinIO Console**: `9001`


