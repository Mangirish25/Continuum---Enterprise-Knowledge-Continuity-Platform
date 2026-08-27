# AGENTS.md — EKCP Coding-Agent Contract

This file is mandatory reading before modifying the repository.

## 1. Mission

Build EKCP as one coherent enterprise product. Prefer simple, explicit, testable boundaries over unnecessary infrastructure.

The implementation must preserve:
- security boundaries,
- source-of-truth boundaries,
- tenant/organization isolation,
- handover state-machine integrity,
- auditability,
- idempotency,
- human approval requirements,
- reproducibility of important AI outputs.

## 2. Documentation precedence

When documents conflict, use this order:

1. `AGENTS.md` — coding-agent constraints
2. `docs/REQUIREMENTS.md` — product requirements
3. `docs/DECISIONS.md` — accepted architecture decisions
4. `docs/ARCHITECTURE.md` — component and dependency architecture
5. `docs/IMPLEMENTATION_STRUCTURE.md` — where new files/modules belong
6. `docs/SECURITY.md` — security rules
7. `docs/AI.md` — AI behavior and governance
8. `docs/DATABASE.md` — persistence contract
9. `docs/API.md` — HTTP contract
10. `docs/CONNECTORS.md` — integration contract
11. `docs/HANDOVER.md` — workflow contract
12. task files — implementation slice
13. `tasks/BOARD.md` — cross-team status index only; if it conflicts with a task file's Status/acceptance criteria, the task file wins
14. `README.md` — orientation only

If a conflict cannot be resolved, stop and document the conflict rather than silently choosing.

## 3. Non-negotiable architecture rules

### Business logic
- API routes/controllers are thin.
- Business rules live in application/domain services.
- Database access is isolated through repositories/data-access modules.
- Agents do not directly access ORM sessions or repositories.
- Workers call application services; they do not duplicate business logic.

### AI
- The LLM is never an authorization component.
- Retrieved enterprise content is untrusted data, not instructions.
- Agents may request tools but cannot bypass policy.
- Sensitive side effects require backend authorization and, where specified, human approval.
- Never let model output directly determine privileged access.
- Important AI outputs must preserve model/prompt/source/version metadata.
- No application module may call an LLM provider directly. All calls go through the internal LLM boundary (see `docs/AI.md` §7).
- All Gemini calls must pass through the centralized Gemini rate-limiting boundary (rolling 60-second RPM/TPM window, UTC-day daily counter, typed `GeminiLimitError`). Do not add a direct Gemini call that bypasses the limiter, and do not remove or weaken the limiter to make a feature or a test pass.

### Security
- Every tenant-owned resource is organization-scoped.
- Authorization is enforced server-side.
- Never rely on frontend checks for security.
- Never put credentials in source code, tests, Docker images, frontend bundles, or Git history.
- Development may use `.env`; production must use an appropriate secret store/deployment secret mechanism.
- Source permission changes and deletions must eventually propagate to indexed knowledge.
- Connectors must use supported source-system APIs (e.g. GitHub GraphQL v4 / REST v3) for targeted metadata/content retrieval. Bulk repository cloning or bulk downloading of a source system to local disk is prohibited unless an explicit ADR permits it. See `docs/CONNECTORS.md` §1.

### Reliability
- Side-effecting operations must be retry-safe.
- Use idempotency keys/unique constraints where repeated requests are possible.
- External integrations must tolerate timeouts, rate limits, partial failure, and retries.
- Long-running operations belong in workers and return job IDs from APIs.

### Audit
- Important business/security changes must be auditable.
- Audit events use canonical serialization and controlled/serialized chain writes.
- Describe the ledger as tamper-evident, not magically immutable.
- PostgreSQL WAL is not the business audit model.
- Do not remove or rewrite audit history to make tests pass.

## 4. Dependency rules

Allowed direction:

`API -> application services -> repositories/models`

`Workers -> application services`

`Agents -> approved tools -> policy/authorization -> services/executors`

`Integrations -> connector contracts + ingestion services`

`RAG -> retrieval/authorization services`

Forbidden:
- API route -> raw SQL for business operations
- Agent -> database
- Agent -> external privileged API
- Frontend -> database
- Connector -> unrelated domain mutation
- LLM provider call scattered across business modules

## 5. Task discipline

Before starting a task:
1. Read its acceptance criteria.
2. Read all declared dependencies.
3. Inspect the relevant architecture document.
4. Reuse existing abstractions.
5. Identify security and audit implications.
6. Plan the smallest vertical slice.

After implementation:
- run relevant tests,
- add missing tests,
- update documentation if behavior changed,
- verify acceptance criteria,
- update the corresponding row in `tasks/BOARD.md`,
- report remaining limitations.

Never mark a task complete merely because code was written.

## 6. Never do this

- Do not introduce microservices just to make the architecture look enterprise-grade.
- Do not introduce Kubernetes unless an explicit decision requires it.
- Do not create duplicate service implementations.
- Do not silently change a database schema without a migration.
- Do not invent API response formats.
- Do not silently weaken authorization to make a demo work.
- Do not use an LLM to calculate deterministic risk metrics that have a defined formula.
- Do not transfer personal credentials between employees.
- Do not call a component "production-ready" without evidence.
- Do not add a dependency without explaining its purpose and impact.
- Do not modify completed task records to hide history.

## 7. Definition of Done

A feature is done only when:
- implementation exists,
- relevant tests exist and pass,
- authorization is enforced,
- error handling is explicit,
- idempotency/retry behavior is addressed where applicable,
- audit behavior is implemented where required,
- documentation matches the implementation,
- acceptance criteria are satisfied,
- no architecture rule is violated.

## 8. Change control

If a change affects a major boundary, persistence model, security model, AI autonomy, deployment architecture, or source-of-truth rule:
1. update/create an ADR in `docs/DECISIONS.md`,
2. update the affected contract document,
3. then implement.

Every ADR in `docs/DECISIONS.md` carries a status: `ACCEPTED`, `PROPOSED`, `IMPLEMENTATION DETAIL`, `NOT REQUIRED`, or `OUT OF SCOPE`. Before changing a technology, framework, or provider named in a document, check its status:
- `ACCEPTED` — do not change without a new/updated ADR.
- `PROPOSED` or `IMPLEMENTATION DETAIL` — may be changed during implementation; note the change in the relevant task.
- `NOT REQUIRED` / `OUT OF SCOPE` — do not build this merely because it appears in a diagram or the Guide.

## 9. Coding style

Prefer:
- small functions,
- explicit types,
- dependency injection,
- structured errors,
- deterministic business logic,
- clear names,
- narrow modules,
- tests close to the behavior they protect.

Avoid clever abstractions until repeated behavior proves the abstraction is needed.
