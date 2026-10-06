# Task 039 — `apps/api/app/ai/agents/coordinator.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 036 (succession agent, as the first real agent to orchestrate), Task 037 (structured output)
**Requirements:** REQ-A003/A004/A006 (coordinated multi-agent workflows), ADR-010 (LangGraph for agent orchestration)
**Board ref:** `tasks/BOARD.md` — Phase 13.1
**Owner:** Mangirish

## Goal

The LangGraph-based Coordinator that delegates to the specialized agents, implementing ADR-010 — chosen specifically for inspectable, debuggable execution traces for the viva.

## Scope

- `apps/api/app/ai/agents/coordinator.py`
- A LangGraph graph wiring the Coordinator node to the specialized agents (Succession — Task 036; Documentation — Task 040; Risk — Task 041; Security — Task 042; Reminder/Notification — Task 043) as the workflow requires.
- Explicit, inspectable state at each step — per ADR-010's rationale, this needs to be genuinely demonstrable in a live defense: able to show the graph's state and decisions at each node, not just a final output.
- Tool-boundary enforcement: agents request tools/data through the Coordinator's defined boundary, never bypassing it to call a database, the LLM Gateway, or a connector directly outside the graph's declared tools (`docs/AI.md` — 'agents may request tools but cannot bypass policy').

## Out of scope

- The individual agents' internal logic — those are Tasks 036, 040–043, built and testable independently; this task wires them together.
- Authorization/policy enforcement logic itself — that remains in the backend (Task 009, Task 033's state machine, etc.); the Coordinator calls through those boundaries, it doesn't reimplement them.

## Implementation notes

- ADR-010's constraint is explicit and important: 'LangGraph orchestrates reasoning/workflow. It does not replace application services, authorization, policy enforcement, or audit.' Keep this strictly architectural line — a tempting shortcut (e.g. letting an agent directly call Task 038's access-review module without going through Task 034's approval-gated API) would violate this and should be refused even if it 'works.'
- This is the component most directly tied to the viva's debuggability requirement — prioritize making a single run's execution trace easy to show and explain over maximizing agent sophistication.

## Acceptance criteria

- [ ] The Coordinator can run a multi-step workflow involving at least the Succession agent (Task 036), with inspectable intermediate state.
- [ ] No agent call bypasses the declared tool boundary to reach a database, LLM provider, or sensitive backend operation directly.
- [ ] A run's execution trace can be shown/exported in a form suitable for a live demonstration.

## Tests

- [ ] Unit — graph wiring/routing logic with mocked agent nodes
- [ ] Integration — a real multi-agent run against real underlying services (within Gemini rate limits)
- [ ] Security — confirm no agent can reach a sensitive write path (e.g. Task 038) without going through its proper approval-gated boundary
- [ ] E2E — a full, demonstrable Coordinator run — this is the first genuinely multi-agent E2E test in the system

## Documentation updates

`docs/AI.md` — confirm the implemented graph structure matches ADR-010's description; update if it had to diverge for a concrete technical reason.

## Known limitations

_Fill in at completion._
