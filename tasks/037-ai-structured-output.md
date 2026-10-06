# Task 037 — `apps/api/app/ai/structured_output.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 007 (knows the DB shapes agent output may need to map to)
**Requirements:** supports REQ-A004 and all later agent tasks (Phase 13), `docs/AI.md` (preserve model/prompt/source/version metadata)
**Board ref:** `tasks/BOARD.md` — Phase 11.2
**Owner:** Mangirish

## Goal

Shared Instructor + Pydantic schemas for every agent's structured output, so agent responses are validated and consistently shaped rather than each agent parsing raw LLM text independently.

## Scope

- `apps/api/app/ai/structured_output.py`
- Base schema(s) every agent output extends, including the metadata `docs/AI.md` requires (model used, prompt version, source references, timestamp).
- Specific schemas for the outputs Phase 11/13 agents need to produce: succession recommendation (Task 036), documentation gap findings (Task 040), risk summary (Task 041), security findings (Task 042), reminder content (Task 043).
- Validation/retry handling for a malformed LLM response (Instructor's structured-output validation failing) — mapped to a typed error (Task 006), not a raw parsing exception.

## Out of scope

- The agents' actual reasoning/prompting logic — this task only defines the output contract they must conform to.

## Implementation notes

- This is shared infrastructure for every Phase 11/13 agent — build it ahead of or alongside Task 036 rather than each agent task defining its own ad hoc schema, which was flagged as exactly the kind of inconsistency the project's documentation-first approach is meant to prevent.

## Acceptance criteria

- [ ] A base schema exists carrying required provenance metadata (model, prompt version, sources, timestamp).
- [ ] Per-agent output schemas exist for at least Task 036's succession recommendation, with room to add the others as those tasks land.
- [ ] A malformed/invalid LLM response is handled as a typed error, not an unhandled exception.

## Tests

- [ ] Unit — schema validation against well-formed and deliberately malformed sample LLM outputs
- [ ] Integration — a real structured call through the LLM Gateway returns a validated schema instance
- [ ] Security — n/a
- [ ] E2E — n/a

## Documentation updates

`docs/AI.md` — reference this module as the canonical structured-output contract if not already implied.

## Known limitations

_Fill in at completion._
