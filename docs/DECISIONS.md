# Architecture Decisions

Use this document as the index of accepted decisions.

## Decision status

Every decision below carries one status. A coding agent must treat these differently:

| Status | Meaning |
|---|---|
| `ACCEPTED` | Locked. Do not change without a new/updated ADR. |
| `PROPOSED` | Under consideration; may still change. |
| `IMPLEMENTATION DETAIL` | May be changed freely during implementation without architectural review. |
| `NOT REQUIRED` | Explicitly not needed now; do not build/introduce it "for completeness." |
| `OUT OF SCOPE` | Excluded from the current implementation even if it appears in a diagram or reference document. |

## Decision summary table

| Decision | Status |
|---|---|
| Modular monolith | ACCEPTED |
| Asynchronous workers | ACCEPTED |
| PostgreSQL as structured system of record | ACCEPTED |
| Vector index as derived/rebuildable state | ACCEPTED |
| Permission-aware RAG | ACCEPTED |
| AI tool/policy boundary | ACCEPTED |
| Human approval for sensitive actions | ACCEPTED |
| Tamper-evident SHA-256 audit ledger | ACCEPTED |
| Formal handover state machine | ACCEPTED |
| Deterministic KCS / bus-factor calculations | ACCEPTED |
| LangGraph for agent orchestration | ACCEPTED |
| Gemini 2.5 Flash-Lite / Groq / LiteLLM provider architecture | ACCEPTED |
| ChromaDB as vector store | ACCEPTED |
| API-only connector access (no bulk clone/download) | ACCEPTED |
| Viva/demo prefetch-and-cache requirement | ACCEPTED |
| Kubernetes | NOT REQUIRED |
| Slack connector | OUT OF SCOPE |

## ADR-001 — Modular monolith + asynchronous workers

**Status:** Accepted

The initial implementation uses a modular monolith for the API/application and asynchronous workers for long-running operations.

**Reason:** Keeps boundaries explicit without creating unnecessary distributed-system complexity.

## ADR-002 — PostgreSQL as structured system of record

**Status:** Accepted

PostgreSQL owns structured continuity, workflow, identity-reference, and audit metadata.

## ADR-003 — Vector index is derived

**Status:** Accepted

Embeddings/vector search are rebuildable derived state. Source systems remain authoritative for source-owned information.

## ADR-004 — Permission-aware RAG

**Status:** Accepted

Semantic relevance is insufficient. Retrieval must respect authorization.

## ADR-005 — AI tool/policy boundary

**Status:** Accepted

Agents cannot directly perform arbitrary privileged actions.

## ADR-006 — Human approval for sensitive actions

**Status:** Accepted

Ownership transfer, access changes and comparable sensitive operations require backend validation and authorized human approval.

## ADR-007 — Tamper-evident audit ledger

**Status:** Accepted

Use a relational audit event model with canonical cryptographic chaining and controlled concurrent writes. Stronger protection may use an external immutable checkpoint.

## ADR-008 — Formal handover state machine

**Status:** Accepted

Handover lifecycle is represented as explicit states and allowed transitions.

## ADR-009 — Deterministic risk calculations

**Status:** Accepted

KCS and bus-factor methodology are explainable deterministic calculations, not opaque LLM-generated scores.

## ADR-010 — LangGraph for agent orchestration

**Status:** Accepted

**Decision:** Use LangGraph as the orchestration framework for multi-step agent workflows (Coordinator delegating to Documentation, Risk, Succession, Security, Reminder/Notification agents).

**Reason:**
- Explicit graph/state representation of a run.
- Inspectable, debuggable execution traces — chosen specifically because the viva/defense requires being able to show *why* an agent did what it did, not just the final output.
- Clear tool-boundary and retry/failure handling per node.
- Easier to demonstrate live than an implicit crew-style handoff.

**Alternatives considered:** CrewAI — rejected primarily for weaker execution-trace visibility in a live-demo/defense context.

**Constraint:** LangGraph orchestrates reasoning/workflow only. It does not replace application services, authorization, policy enforcement, or the audit ledger — those remain deterministic backend components that agents call through the tool/policy boundary (`docs/AI.md` §3).

**Implementation reference:** orchestration graph lives under `backend/app/ai/` (or `apps/api/app/ai/` per `docs/IMPLEMENTATION_STRUCTURE.md`).

## ADR-011 — LLM provider architecture

**Status:** Accepted

**Decision:**

```text
                         ┌─ Gemini 2.5 Flash-Lite  (primary generation)
                         │
Application → LLM Gateway ┼─ Groq (Llama 3.3 70B)  (short-prompt routing, latency-sensitive)
                         │
                         └─ LiteLLM               (provider abstraction / fallback routing)

LLM Gateway → Gemini Rate Limiter (rolling 60s RPM/TPM window, UTC-day daily reset, typed GeminiLimitError)
```

- **Gemini 2.5 Flash-Lite** is the primary model — selected for free-tier TPM headroom (~1,000,000 TPM) versus alternatives like Groq (~12,000 TPM), which matters for multi-agent chaining in a live demo.
- **Groq** is used selectively for short-prompt routing steps where latency matters, not for main synthesis.
- **LiteLLM** is the fallback routing layer for graceful degradation if a primary provider is unavailable or rate-limited.
- Two separate Google API keys are held as a practical demo-day safety net against rate-limit exhaustion.

**Rule:** No application module may call an LLM provider directly. All calls go through the internal LLM Gateway, which enforces the Gemini rate limiter before any Gemini call. This is what `gemini_client.py` and `gemini_rate_limiter.py` already implement — new code must go through the same boundary rather than calling a provider SDK directly.

**Implementation reference:** `gemini_client.py`, `gemini_rate_limiter.py`.

## ADR-012 — ChromaDB as vector store

**Status:** Accepted

**Decision:** Use ChromaDB for embeddings/semantic retrieval, combined with BM25 lexical search via Reciprocal Rank Fusion (hybrid retrieval).

```text
PostgreSQL      → source metadata, authorization metadata, system of record
Object storage  → large source assets (files, documents)
ChromaDB        → derived embeddings / semantic retrieval (hybrid with BM25 + RRF)
```

ChromaDB holds **derived, rebuildable state only** (per ADR-003). It is not a source of truth and must be reconstructable from source metadata/content if lost.

## ADR-013 — API-only connector access

**Status:** Accepted

**Decision:** Connectors retrieve data exclusively through supported source-system APIs (e.g. GitHub GraphQL v4 for a single round-trip README/issues/PR-comments query, REST v3 for the file tree). Bulk cloning or bulk-downloading a source system to local disk is prohibited unless a future ADR explicitly permits it for a specific, documented reason.

**Reason:** Keeps the platform's footprint on source systems minimal and auditable, avoids storing an unmanaged full copy of third-party data, and keeps ingestion jobs fast and rate-limit-friendly.

**Implementation reference:** `github_connector.py`.

## ADR-014 — Viva/demo prefetch-and-cache requirement

**Status:** Accepted

**Decision:** The viva/demo path must not depend on live external API availability. Required external data and AI outputs must be prefetched, cached, or otherwise made deterministic before the demonstration.

```text
Development integration mode → live APIs allowed
Viva/demo mode                → live external dependencies prohibited
```

This is a hard requirement, not a "where appropriate" preference — see `docs/DEMO.md`. It exists because demo stability during a live academic defense is a first-class constraint: a rate-limit error, a flaky third-party API, or network latency during the viva is treated as equivalent in severity to a functional bug.

## ADR template

### ADR-NNN — Title
- Status:
- Context:
- Decision:
- Alternatives:
- Consequences:
- Requirements affected:
- Date:
