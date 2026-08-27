# API Contract

## 1. Versioning

Use `/api/v1/...`.

## 2. Groups

### Auth
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

### Users
- `GET /api/v1/users`
- `GET /api/v1/users/{id}`
- `PATCH /api/v1/users/{id}`

### Projects
- `GET /api/v1/projects`
- `POST /api/v1/projects`
- `GET /api/v1/projects/{id}`
- `GET /api/v1/projects/{id}/risk`

### Assets
- `POST /api/v1/assets`
- `GET /api/v1/assets`
- `GET /api/v1/assets/{id}`
- `PATCH /api/v1/assets/{id}`

### Knowledge
- `POST /api/v1/knowledge/ingest`
- `GET /api/v1/knowledge/documents`
- `POST /api/v1/search`

### Handovers
- `POST /api/v1/handovers`
- `GET /api/v1/handovers`
- `GET /api/v1/handovers/{id}`
- `POST /api/v1/handovers/{id}/approve`
- `POST /api/v1/handovers/{id}/complete`

### Audit
- `GET /api/v1/audit/events`
- `POST /api/v1/audit/verify`

### Integrations
- `POST /api/v1/integrations/{provider}/connect`
- `GET /api/v1/integrations/status`

### Jobs
- `GET /api/v1/jobs/{job_id}`

## 3. Long-running operations

Return `202 Accepted` with a job ID.

```json
{
  "job_id": "..."
}
```

Poll:

```text
GET /api/v1/jobs/{job_id}
```

Statuses:
`PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED`.

## 4. Error contract

```json
{
  "error": {
    "code": "permission_denied",
    "message": "You do not have access to this resource.",
    "request_id": "..."
  }
}
```

Standard categories:
- validation_error
- authentication_required
- permission_denied
- resource_not_found
- state_conflict
- business_rule_violation
- rate_limited
- dependency_unavailable
- internal_error

## 5. API rules

- Never expose internal stack traces.
- Never trust client-provided organization ownership.
- Enforce authorization before returning data.
- Use pagination for collections.
- Use idempotency keys for retryable side effects.
- Keep routes thin and delegate business logic.
