# Testing Strategy

## Unit tests

Cover:
- domain rules,
- KCS,
- bus factor,
- state transitions,
- policy decisions,
- audit hashing,
- idempotency behavior.

## Integration tests

Cover:
- database repositories,
- authorization + RLS,
- connector normalization,
- ingestion pipeline,
- job processing,
- API contracts.

## Security tests

Every authorization-sensitive feature must include negative tests:
- wrong organization,
- wrong role,
- inaccessible project/resource,
- inaccessible RAG document,
- revoked source permission.

## E2E tests

At minimum, exercise the critical story:

```text
employee leaves
 -> continuity/risk assessment
 -> handover created
 -> knowledge package
 -> successor recommendation
 -> approval
 -> ownership/access actions
 -> verification
 -> audit
```

## AI evaluation

Keep a fixed evaluation set for:
- retrieval,
- groundedness,
- citation quality,
- authorization leakage,
- prompt injection resistance.

## Definition of done

A feature without relevant tests is incomplete unless the task explicitly documents why a test is not practical.
