# Build Board

**Status:** index only — **not authoritative.**

This file is a cross-team status view, not a source of truth. If a row here
conflicts with a task file's `Status:` or `Acceptance criteria`, the task
file wins (see `AGENTS.md` §2).

Tick a box only when the corresponding task's acceptance criteria are met
and the change is merged — not when code is merely written (see `AGENTS.md`
§5, §7). This is the same "update the board" step listed in the
after-implementation checklist.

Format: `- [ ] <phase.order> — <owner> — \`path\` — description`

Owners: **Mangirish** (RAG · GenAI · Agents) · **Rahul** (Frontend) ·
**Sanmati** (Backend) · **Paras** (DevOps · Testing)

File paths follow `docs/IMPLEMENTATION_STRUCTURE.md`. Phase numbers follow
the 17-step build order below (this section). Items in the same phase can
generally be worked in parallel; a phase's note explains what it depends on.

---

## Phase 1 — Foundation + scaffolding
_No dependencies — can start day one._

- [x] 1.1 — Paras — `infra/docker/api.Dockerfile` — Base API container image ([task](001-api-dockerfile.md))
- [x] 1.2 — Paras — `infra/docker/web.Dockerfile` — Base web container image ([task](002-web-dockerfile.md))
- [x] 1.3 — Paras — `infra/compose/docker-compose.yml` — Postgres, Redis, MinIO, API, web wired together ([task](003-docker-compose.md))
- [x] 1.4 — Paras — `infra/secrets/.env.example` — Documented env vars, no real secrets ([task](004-env-example.md))
- [x] 1.5 — Sanmati — `apps/api/app/core/config.py` — Settings/env loading ([task](005-core-config.md))
- [x] 1.6 — Sanmati — `apps/api/app/core/exceptions.py` — Typed error base classes (no raw exceptions to clients) ([task](006-core-exceptions.md))

## Phase 2 — Database + migrations
_Depends on phase 1 (docker/config)._

- [ ] 2.1 — Sanmati — `apps/api/app/repositories/models/*.py` — ORM models: org, user, project, asset, handover, risk, audit_event
- [ ] 2.2 — Sanmati — `migrations/0001_initial_schema.py` — Alembic initial migration

## Phase 3 — Identity + org authorization
_Depends on phase 2._

- [ ] 3.1 — Sanmati — `apps/api/app/core/security.py` — JWT issuing/verification, RBAC checks
- [ ] 3.2 — Sanmati — `apps/api/app/api/v1/auth.py` — Login, token refresh, MFA hook

## Phase 4 — Projects / assets / ownership
_Depends on phase 3._

- [ ] 4.1 — Sanmati — `apps/api/app/repositories/project_repository.py`
- [ ] 4.2 — Sanmati — `apps/api/app/repositories/asset_repository.py`
- [ ] 4.3 — Sanmati — `apps/api/app/api/v1/projects.py` — CRUD + ownership endpoints
- [ ] 4.4 — Sanmati — `apps/api/app/api/v1/assets.py`

## Phase 5 — Audit ledger
_Depends on phase 2. Unblocks everything that writes state._

- [ ] 5.1 — Sanmati — `apps/api/app/audit/ledger.py` — SHA-256 hash-chained event writer (ADR-007)
- [ ] 5.2 — Sanmati — `apps/api/app/audit/verification.py` — Chain verification job

## Phase 6 — Frontend shell
_Can start against a mocked API once phase 1 lands._

- [ ] 6.1 — Rahul — `apps/web/src/api/client.ts` — HTTP client, auth header wiring
- [ ] 6.2 — Rahul — `apps/web/src/types/index.ts` — Shared TS types matching backend schemas
- [ ] 6.3 — Rahul — `apps/web/src/hooks/useAuth.ts`
- [ ] 6.4 — Rahul — `apps/web/src/components/layout/AppShell.tsx` — Nav, layout scaffold
- [ ] 6.5 — Rahul — `apps/web/src/pages/Dashboard.tsx`
- [ ] 6.6 — Rahul — `apps/web/src/features/projects/ProjectList.tsx` — Depends on phase 4 API
- [ ] 6.7 — Rahul — `apps/web/src/features/employees/EmployeeList.tsx`

## Phase 7 — One connector end-to-end
_GitHub already implemented — reference for the rest._

- [x] 7.1 — Sanmati — `apps/api/app/integrations/github_connector.py` — GraphQL v4 + REST v3, API-only (ADR-013)
- [ ] 7.2 — Sanmati — `apps/api/app/workers/ingestion_worker.py` — Async job: connector → normalize → store

## Phase 8 — Knowledge / RAG
_Depends on phase 7 (needs at least one connector feeding data)._

- [x] 8.1 — Mangirish — `apps/api/app/ai/gemini_client.py` — LLM Gateway → Gemini boundary
- [x] 8.2 — Mangirish — `apps/api/app/ai/gemini_rate_limiter.py` — Rolling 60s RPM/TPM, UTC-day reset
- [ ] 8.3 — Mangirish — `apps/api/app/rag/chunking.py`
- [ ] 8.4 — Mangirish — `apps/api/app/rag/embeddings.py`
- [ ] 8.5 — Mangirish — `apps/api/app/rag/hybrid_retrieval.py` — BM25 + dense vector via RRF (ChromaDB, ADR-012)
- [ ] 8.6 — Mangirish — `apps/api/app/rag/permission_filter.py` — Permission-aware retrieval (REQ-S002)
- [ ] 8.7 — Rahul — `apps/web/src/features/knowledge-assistant/ChatInterface.tsx` — Depends on RAG endpoint existing

## Phase 9 — KCS + bus factor
_Depends on phases 4, 7._

- [ ] 9.1 — Sanmati — `apps/api/app/modules/risk/bus_factor_engine.py` — Deterministic — not LLM-driven (`docs/AI.md`)
- [ ] 9.2 — Sanmati — `apps/api/app/modules/risk/doc_divergence_detector.py` — Code/doc staleness signals
- [ ] 9.3 — Rahul — `apps/web/src/features/risk/RiskDashboard.tsx`

## Phase 10 — Handover workflow
_Depends on phases 4, 5._

- [ ] 10.1 — Sanmati — `apps/api/app/modules/handover/state_machine.py` — Formal handover states (ADR)
- [ ] 10.2 — Sanmati — `apps/api/app/api/v1/handovers.py`
- [ ] 10.3 — Rahul — `apps/web/src/features/handover/HandoverWizard.tsx`

## Phase 11 — Succession recommendation
_Depends on phases 8, 9._

- [ ] 11.1 — Mangirish — `apps/api/app/ai/agents/succession_agent.py` — Explainable, human-approved (REQ-A004)
- [ ] 11.2 — Mangirish — `apps/api/app/ai/structured_output.py` — Instructor/Pydantic schemas for agent outputs

## Phase 12 — Controlled ownership / access workflow
_Depends on phases 10, 11._

- [ ] 12.1 — Sanmati — `apps/api/app/modules/handover/access_review.py` — Human-approved access changes

## Phase 13 — Coordinator + supporting agents
_Depends on phase 11._

- [ ] 13.1 — Mangirish — `apps/api/app/ai/agents/coordinator.py` — LangGraph orchestration (ADR-010)
- [ ] 13.2 — Mangirish — `apps/api/app/ai/agents/documentation_agent.py`
- [ ] 13.3 — Mangirish — `apps/api/app/ai/agents/risk_agent.py` — Summarizes deterministic risk output
- [ ] 13.4 — Mangirish — `apps/api/app/ai/agents/security_agent.py`

## Phase 14 — Notifications
_Depends on phase 13._

- [ ] 14.1 — Mangirish — `apps/api/app/ai/agents/reminder_agent.py`
- [ ] 14.2 — Sanmati — `apps/api/app/api/v1/notifications.py`

## Phase 15 — Reliability / security hardening
_Can proceed in parallel once core pieces exist._

- [ ] 15.1 — Paras — `apps/api/tests/` — Pytest harness + fixtures (unit/integration/security)
- [ ] 15.2 — Paras — `apps/web/tests/` — Frontend test harness
- [ ] 15.3 — Paras — `apps/api/tests/test_gemini_rate_limiter.py` — Rate-limit boundary is load-tested, not just unit-tested
- [ ] 15.4 — Paras — `.github/workflows/ci.yml` — CI pipeline: lint, test, build
- [ ] 15.5 — Sanmati — `apps/api/app/core/security.py#webhooks` — Webhook validation (REQ-S005)

## Phase 16 — Additional connectors
_Depends on phase 7's pattern being proven._

- [ ] 16.1 — Sanmati — `apps/api/app/integrations/jira_connector.py` — Atlassian API token auth
- [ ] 16.2 — Sanmati — `apps/api/app/integrations/confluence_connector.py`
- [ ] 16.3 — Sanmati — `apps/api/app/integrations/gdrive_connector.py` — OAuth 2.0 installed-app flow

## Phase 17 — Demo hardening
_Last — depends on everything above being functional at least once._

- [ ] 17.1 — Paras — `scripts/prefetch_demo_data.py` — Pre-fetch + cache all connector/LLM output before viva (ADR-014)
- [ ] 17.2 — Paras — `infra/monitoring/logging_config.py` — Clean, professional-looking logs for live demo
- [ ] 17.3 — Rahul — `apps/web/src/features/admin/AdminPanel.tsx`
- [ ] 17.4 — Mangirish — `apps/api/app/rag/evaluation_set.py` — Retrieval/groundedness eval set (REQ-A005)
