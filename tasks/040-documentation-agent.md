# Task 040 — `apps/api/app/ai/agents/documentation_agent.py`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 031 (doc divergence detector), Task 028 (retrieval), Task 037 (structured output)
**Requirements:** REQ-A003 (compare code/project signals with documentation, identify gaps)
**Board ref:** `tasks/BOARD.md` — Phase 13.2
**Owner:** Mangirish

## Goal

An LLM-driven agent that takes Task 031's deterministic staleness signal and produces a human-readable explanation of what's missing or outdated and why it matters.

## Scope

- `apps/api/app/ai/agents/documentation_agent.py`
- Reads Task 031's divergence findings plus permission-filtered retrieved content (Task 028), and produces a structured (Task 037) explanation of documentation gaps.
- Calls the LLM Gateway only, respecting rate limits.

## Out of scope

- Detecting the staleness signal itself — that's Task 031's deterministic job; this agent explains and contextualizes it, consistent with ADR-009's separation of deterministic calculation from AI narrative.

## Implementation notes

- Keep this agent's output clearly distinguishable as an AI-generated explanation of a deterministic finding, not itself the source of truth for whether something is actually stale (that's Task 031).

## Acceptance criteria

- [ ] Given Task 031's real findings, produces a clear, structured, human-readable explanation per document/gap.
- [ ] Output conforms to Task 037's schema, including provenance metadata.

## Tests

- [ ] Unit — agent logic against mocked findings and a mocked LLM response
- [ ] Integration — real call through the LLM Gateway against real Task 031 output
- [ ] Security — confirm retrieved content used as context is treated as untrusted data, not instructions, per `docs/AI.md`
- [ ] E2E — deferred to Task 039 (Coordinator) integration

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
