# Task 029 — `apps/web/src/features/knowledge-assistant/ChatInterface.tsx`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 028 (permission-aware retrieval), Task 017 (api client), Task 020 (AppShell)
**Requirements:** REQ-A001 (index/search enterprise knowledge, ask questions)
**Board ref:** `tasks/BOARD.md` — Phase 8.7
**Owner:** Rahul

## Goal

The user-facing Knowledge Assistant chat UI — the first feature where a user directly interacts with the RAG pipeline, with cited sources.

## Scope

- `apps/web/src/features/knowledge-assistant/ChatInterface.tsx`
- A chat UI sending queries to whatever backend endpoint wraps Task 027/028 (confirm with Mangirish/Sanmati which module exposes this as an HTTP route — if none exists yet, that's a small missing API task worth flagging rather than building against a non-existent endpoint).
- Displays responses with cited sources (document/chunk references) — per `docs/AI.md`, 'important AI outputs must preserve model/prompt/source/version metadata,' and the UI should surface that provenance, not hide it.
- Handles the case where retrieval returns nothing relevant/authorized gracefully (not a confusing empty response).

## Out of scope

- Multi-turn conversation memory/context beyond what's needed for a working single-session chat — a stateless-per-query design is acceptable for this phase unless already decided otherwise.
- Streaming responses — a clean non-streaming request/response cycle is sufficient; streaming is a polish item for later if time allows.

## Implementation notes

- This is the most demo-visible feature in the whole system — `docs/DEMO.md`'s prefetch/cache requirement (ADR-014) will specifically apply to this feature during the viva. Build it now against live calls for development, but keep in mind Task 053 will need a way to drive this UI off prefetched/cached responses for the actual presentation.

## Acceptance criteria

- [ ] A user can ask a question and receive a response with cited sources.
- [ ] A query returning no authorized/relevant results is handled with a clear, non-broken UI state.
- [ ] Errors from the backend (including a rate-limited Gemini call, per the project's known rate-limit ceiling) surface as a clear message, not a silent failure or raw error.

## Tests

- [ ] Unit — component renders given sample chat responses, including the no-results and error cases
- [ ] Integration — a real query against the full backend pipeline (Tasks 025–028 plus whatever LLM synthesis step exists) returns a cited response
- [ ] Security — confirm no unauthorized source content ever appears in a rendered response or its citations
- [ ] E2E — login → ask a question → see a cited answer, against the real stack

## Documentation updates

None expected.

## Known limitations

_Fill in at completion — note explicitly which backend endpoint this calls, since it isn't yet a separately tracked task on the board._
