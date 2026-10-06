# Task 041 — `apps/api/app/ai/agents/risk_agent.py`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 030 (bus-factor/KCS engine), Task 037 (structured output)
**Requirements:** REQ-A003 (summarize continuity risk indicators)
**Board ref:** `tasks/BOARD.md` — Phase 13.3
**Owner:** Mangirish

## Goal

Summarizes Task 030's deterministic risk scores in natural language — explicitly a summarizer, never the source of the score itself, per ADR-009 and the prior agent-roster reconciliation decision that 'risk agent summarizes deterministic output; it does not compute it.'

## Scope

- `apps/api/app/ai/agents/risk_agent.py`
- Reads Task 030's real `risk_assessments` data and produces a structured (Task 037) natural-language summary/explanation.

## Out of scope

- Any calculation of bus-factor/KCS itself — strictly Task 030's responsibility. If this agent finds itself computing a number rather than explaining one, that's a scope violation to flag, not silently proceed with.

## Implementation notes

- This is the clearest example in the whole agent roster of the deterministic-vs-AI-narrative split — keep the boundary explicit in code (e.g. the agent's input is already-computed scores, never raw project data it could compute a score from itself).

## Acceptance criteria

- [ ] Given real Task 030 output, produces a clear, structured summary.
- [ ] The agent never computes a risk score itself — only explains an existing one.

## Tests

- [ ] Unit — summary generation against sample risk-assessment data
- [ ] Integration — real call through the LLM Gateway against real Task 030 output
- [ ] Security — n/a beyond standard untrusted-content handling
- [ ] E2E — deferred to Task 039 integration

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
