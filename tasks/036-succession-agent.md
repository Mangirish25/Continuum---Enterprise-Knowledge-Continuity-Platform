# Task 036 — `apps/api/app/ai/agents/succession_agent.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 027/028 (retrieval), Task 030 (bus-factor/risk data), Task 037 (structured output schemas)
**Requirements:** REQ-A004 (AI-assisted succession recommendation, explainable, human-approved)
**Board ref:** `tasks/BOARD.md` — Phase 11.1
**Owner:** Mangirish

## Goal

An LLM-driven agent that compares a departing employee's responsibilities/skills against potential successors and produces an explainable recommendation — never an autonomous decision, per `docs/AI.md`'s human-in-the-loop principle.

## Scope

- `apps/api/app/ai/agents/succession_agent.py`
- Reads relevant project/skill/ownership data (via Task 011/030 and permission-filtered retrieval, Task 028) to identify candidate successors.
- Produces a structured recommendation (via Task 037's schema) with an explicit rationale — the explanation is not optional decoration; `docs/AI.md` requires important AI outputs to preserve model/prompt/source/version metadata, and this recommendation must be defensible in a viva.
- All LLM calls go through the LLM Gateway (`gemini_client.py`/`gemini_rate_limiter.py`) — no direct provider calls, per `AGENTS.md`'s non-negotiable rule.

## Out of scope

- Actually executing any ownership/access change based on the recommendation — that remains strictly human-approved (Task 034's approval step, Task 038's access execution). This agent only recommends.
- LangGraph orchestration wiring — Task 039 (Coordinator) is what invokes this agent as a node/tool; this task builds the agent's own logic, callable independently for testing.

## Implementation notes

- Respect the Gemini rate-limit ceiling (15 RPM / 250,000 TPM / ~1,000 RPD soft cap, 4.0–4.5s inter-call delay) — a succession recommendation over multiple candidates should batch/structure its calls to stay well within this, not assume unlimited throughput.
- The never-reversed rule applies here as everywhere: the LLM is never an authorization component (`docs/AI.md`) — this agent's output is a suggestion for a human to approve via Task 034, not an executable instruction.

## Acceptance criteria

- [ ] Given real project/skill/risk data, produces a structured recommendation with a clear, human-readable rationale.
- [ ] Recommendation output includes source/model/prompt-version metadata per `docs/AI.md`.
- [ ] No direct Gemini/LLM provider calls bypass the rate-limited LLM Gateway.
- [ ] The agent is callable and testable independently of the full LangGraph Coordinator.

## Tests

- [ ] Unit — agent logic against mocked retrieval/risk data and a mocked LLM response
- [ ] Integration — a real call through the LLM Gateway against real underlying data (respecting rate limits during test runs)
- [ ] Security — confirm the agent cannot be prompted (via injected document content, since retrieved content is untrusted per `docs/AI.md`) into recommending or executing a privileged action directly
- [ ] E2E — deferred to Phase 13 (Coordinator) for full multi-agent flow

## Documentation updates

`docs/AI.md` — note if this task reveals the agent roster/capability split (established in prior reconciliation work) needs adjustment.

## Known limitations

_Fill in at completion._
