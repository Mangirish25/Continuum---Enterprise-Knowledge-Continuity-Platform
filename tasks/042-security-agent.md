# Task 042 — `apps/api/app/ai/agents/security_agent.py`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 038 (access review data), Task 033 (handover state), Task 037 (structured output)
**Requirements:** REQ-A003 (highlight access, offboarding, sensitive-asset issues)
**Board ref:** `tasks/BOARD.md` — Phase 13.4
**Owner:** Mangirish

## Goal

Highlights access/offboarding/sensitive-asset concerns during a handover for human review — an advisory flag, never an enforcement action itself.

## Scope

- `apps/api/app/ai/agents/security_agent.py`
- Reads handover/access state (Task 033/038) and permission-filtered asset classification data to flag concerns (e.g. a departing user retains access to a sensitive asset with no successor assigned) as structured (Task 037) output for a human reviewer.

## Out of scope

- Executing any access change itself — strictly Task 038's job, strictly after human approval. This agent only flags.

## Implementation notes

- Same human-in-the-loop boundary as every other agent touching access/security: this agent's output is a flag for a human, never an executable instruction, per `docs/AI.md`.

## Acceptance criteria

- [ ] Given real handover/access/asset data, produces structured, actionable flags for human review.
- [ ] No code path in this agent directly triggers an access change.

## Tests

- [ ] Unit — flagging logic against synthetic scenarios with known expected concerns
- [ ] Integration — real call through the LLM Gateway against real handover data
- [ ] Security — confirm this agent has no code path capable of calling Task 038 directly — only flags for human review via the normal approval-gated API
- [ ] E2E — deferred to Task 039 integration

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
