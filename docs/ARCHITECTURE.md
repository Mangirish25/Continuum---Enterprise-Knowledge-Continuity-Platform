# Architecture

## 1. Architectural style

Use a **modular monolith + asynchronous workers** initially.

The application is one deployable backend with explicit module boundaries. Long-running work runs through workers. Do not split modules into microservices unless a documented decision requires it.

## 2. High-level flow

```text
React UI
   |
FastAPI API
   |
+--+-------------------+------------------+
|                      |                  |
Domain Services     Knowledge/RAG      AI Tools
|                      |                  |
Repositories        Vector Index       Policy Gate
|                      |                  |
PostgreSQL         Object Storage       Executors
|
Audit Service
|
Audit Ledger -> optional external checkpoint
```

## 3. Backend boundaries

```text
backend/app/
├── core/             # configuration, DB, logging, dependencies
├── api/              # HTTP transport only
├── modules/          # business capabilities
├── repositories/     # persistence access
├── integrations/     # external systems
├── ai/               # agents, tools, policies, providers
├── rag/              # ingestion/retrieval pipeline
├── workers/          # asynchronous jobs
└── audit/            # audit ledger and verification
```

## 4. Dependency direction

```text
API
 |
Services / domain modules
 |
Repositories
 |
PostgreSQL

Workers -> Services
Agents -> Tools -> Policy -> Services/Executors
Integrations -> Connector contracts -> Ingestion services
RAG -> Authorization + retrieval services
```

## 5. Core modules

- identity
- organizations
- projects
- assets
- knowledge
- risk
- handover
- succession
- notifications
- integrations
- audit

## 6. Deterministic vs AI logic

Deterministic:
- KCS calculation
- bus-factor methodology
- authorization
- state transitions
- idempotency
- audit hashing
- policy enforcement

AI-assisted:
- summarization
- documentation-gap analysis
- semantic retrieval generation
- explainable recommendations
- natural-language synthesis

AI may explain deterministic results; it must not replace deterministic rules where a defined formula/policy exists.

## 7. Source-system boundary

EKCP must not silently become the authoritative source for data owned by GitHub/Jira/Drive/IdP. Store source references, versions and normalized data according to policy.
