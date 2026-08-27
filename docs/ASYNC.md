# Asynchronous Processing

## When to use workers

Use workers for:
- connector synchronization
- ingestion
- parsing/extraction
- embedding
- indexing
- risk recalculation
- document analysis
- notifications
- scheduled reconciliation

## Job lifecycle

```text
API request
  -> create job
  -> queue
  -> worker
  -> service
  -> result/status
```

## Job metadata

At minimum:
- job_id
- job_type
- organization_id
- status
- attempt_count
- created_at
- started_at
- completed_at
- last_error
- correlation_id

## Retry policy

Retries must be bounded and distinguish:
- transient errors
- permanent validation errors
- authorization errors
- rate limits
- dependency outages

## Idempotency

A retry must not duplicate:
- ownership transfers
- access changes
- approvals
- webhook side effects
- notifications
- ingestion records
- audit events

Use idempotency keys and database uniqueness constraints where appropriate.

## Failure handling

Persist failure state. Do not silently swallow exceptions.

Jobs that repeatedly fail should become inspectable and, where useful, dead-lettered for operator action.
