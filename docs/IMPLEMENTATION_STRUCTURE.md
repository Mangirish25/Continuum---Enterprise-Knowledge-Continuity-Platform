# Implementation Structure

The target implementation should make it obvious where logic belongs.

```text
EKCP/
├── apps/
│   ├── api/
│   │   ├── app/
│   │   │   ├── core/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   ├── modules/
│   │   │   ├── repositories/
│   │   │   ├── integrations/
│   │   │   ├── rag/
│   │   │   ├── ai/
│   │   │   ├── workers/
│   │   │   └── audit/
│   │   └── tests/
│   └── web/
│       ├── src/
│       │   ├── features/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── api/
│       │   ├── hooks/
│       │   └── types/
│       └── tests/
├── migrations/
├── infra/
│   ├── docker/
│   ├── compose/
│   ├── monitoring/
│   └── secrets/
├── scripts/
├── tasks/
└── docs/
```

## Placement rules

- HTTP transport -> `api/`
- Business/domain logic -> `modules/`
- Persistence -> `repositories/`, `models/`, migrations
- External systems -> `integrations/`
- Knowledge ingestion/retrieval -> `rag/`
- AI behavior -> `ai/`
- Background execution -> `workers/`
- Audit ledger -> `audit/`
- Deployment/operations -> `infra/`
- Architecture decisions -> `docs/`

Do not create a new top-level architectural category without an ADR.
