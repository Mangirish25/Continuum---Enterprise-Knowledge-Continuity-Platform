# AI Architecture and Governance

## 1. Principle

AI is an intelligence/reasoning layer inside a governed application. It is not the authorization, database, or policy engine.

## 2. Components

### Agents (orchestrated via LangGraph — ADR-010)

- Coordinator — manages multi-step workflows and delegates to the agents below.
- Documentation — compares project/code signals with documentation and identifies gaps or outdated material.
- Risk — explains/summarizes continuity indicators (does not compute them — see §10).
- Succession — matches skills/responsibilities to potential successors, produces an explainable recommendation.
- Security — highlights access, offboarding and sensitive-asset issues.
- Reminder/Notification — monitors deadlines and pending handover actions.

### Platform capabilities (not agents)

These support the agents above but are deterministic services, not LLM-driven graph nodes:

- **RAG/Search** — permission-aware retrieval service (see §5). Agents call it as a tool; it is not itself an agent with independent reasoning.
- **Audit/Compliance** — the audit ledger and its verification logic are deterministic infrastructure (`docs/DATABASE.md` §8), not an AI agent. An agent may *summarize* audit findings via the platform capability, but the ledger itself must never be LLM-driven.

Not every capability needs an LLM. Deterministic engines remain normal application code.

## 3. Tool boundary

```text
Agent
  -> Tool request
  -> Policy gate
  -> Authorization
  -> Human approval if required
  -> Executor
  -> Audit
```

Agents never directly execute privileged external operations.

## 4. AI autonomy

### Level 0 — informational
Search, summarize, classify, explain.

### Level 1 — low-risk automation
Create reminders/tasks, trigger indexing, flag findings, subject to policy.

### Level 2 — controlled action
Ownership/access/handover actions. Human approval required.

### Level 3 — prohibited
Privileged access grants, personal credential transfer, employment decisions, security-policy override. Never autonomous.

## 5. RAG

```text
User
 -> identity/authorization
 -> permission-aware retrieval
 -> relevant authorized chunks
 -> LLM
 -> answer + citations
```

The vector index is not the authorization layer.

Retrieved content is untrusted and must not override system/developer instructions.

## 6. Provenance

Important AI outputs should record:
- model/provider,
- model version,
- prompt version,
- schema version,
- retrieval/source IDs,
- timestamp,
- request/correlation ID.

## 7. LLM provider boundary

Application code should depend on an internal LLM interface rather than scattering provider-specific calls across modules.

**Provider architecture (ADR-011):**

```text
Application → LLM Gateway → Gemini 2.5 Flash-Lite   (primary generation)
                          → Groq (Llama 3.3 70B)     (short-prompt routing)
                          → LiteLLM                  (fallback/provider abstraction)

LLM Gateway → Gemini Rate Limiter                    (rolling 60s RPM/TPM, UTC-day reset)
```

No application module may call an LLM provider SDK directly. All Gemini traffic passes through the rate limiter first; a bypassed call is an architecture violation even if it "works" locally. See `gemini_client.py` and `gemini_rate_limiter.py` for the reference implementation, and `AGENTS.md` §3 (AI) for the corresponding non-negotiable rule.

## 8. Evaluation

Maintain an evaluation set for:
- retrieval relevance,
- authorization leakage,
- groundedness,
- citation correctness,
- hallucination,
- structured-output validity.

## 9. Successor recommendation

The AI may recommend and explain candidates based on authorized project/skill/context data. It must not autonomously make employment decisions or execute a transfer.

## 10. Deterministic analytics

KCS and bus-factor calculations are deterministic and explainable. AI may summarize the findings but should not replace the defined calculation.
