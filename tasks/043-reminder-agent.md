# Task 043 — `apps/api/app/ai/agents/reminder_agent.py`

**Status:** backlog
**Priority:** P2
**Depends on:** Task 033 (handover state — needs deadlines/pending actions to monitor), Task 037 (structured output)
**Requirements:** REQ-A003 (monitor deadlines and pending handover actions)
**Board ref:** `tasks/BOARD.md` — Phase 14.1
**Owner:** Mangirish

## Goal

Monitors pending handover actions/deadlines and produces reminder content — a lightweight agent compared to Phase 13's others.

## Scope

- `apps/api/app/ai/agents/reminder_agent.py`
- Reads pending/overdue handover states and produces structured reminder content (Task 037) for Task 044 to deliver.

## Out of scope

- Actual notification delivery (email, in-app, etc.) — Task 044.
- Scheduling/triggering mechanism — note as a follow-up (e.g. periodic job) rather than building full scheduling infra in this task unless trivial to add.

## Implementation notes

- This is a lower-priority, lighter-weight agent than Phase 13's core four — don't over-invest relative to its actual importance to the demo narrative.

## Acceptance criteria

- [ ] Given real pending/overdue handover data, produces structured reminder content.

## Tests

- [ ] Unit — reminder content generation against sample pending-action data
- [ ] Integration — real call through the LLM Gateway
- [ ] Security — n/a
- [ ] E2E — deferred to Task 044

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
