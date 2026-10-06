# Task 053 — `scripts/prefetch_demo_data.py`

**Status:** backlog
**Priority:** P0
**Depends on:** every connector (Task 024/050/051/052) and the RAG/agent pipeline (Phase 8/13) being functional at least once
**Requirements:** ADR-014 (viva/demo prefetch-and-cache requirement — hard requirement, not 'where appropriate')
**Board ref:** `tasks/BOARD.md` — Phase 17.1
**Owner:** Paras

## Goal

A script that pre-fetches and caches every piece of external data and AI output the demo script will use, so the viva path has zero live external dependencies, per ADR-014.

## Scope

- `scripts/prefetch_demo_data.py`
- Runs the real connectors/ingestion (Task 024 + Phase 16) and real RAG/agent calls (Phase 8/13) once, ahead of time, and persists the results in a form the application can serve in 'viva mode' (per Task 005's `APP_MODE` setting) without re-calling any live external API or LLM provider during the actual presentation.
- Covers the specific demo script's needs end-to-end: whichever project/handover/chat-query flow will actually be shown live.

## Out of scope

- General-purpose caching infrastructure for production use — this is viva-specific tooling, not a production caching layer.

## Implementation notes

- This is the direct implementation of ADR-014 and the project's single most-repeated principle: demo stability over completeness. Treat any live dependency surviving into the actual demo run as a release blocker, not a minor gap.
- Coordinate with whoever owns the actual demo script/narrative to know exactly which flows need to be prefetched — don't guess at scope here.

## Acceptance criteria

- [ ] Running this script once produces everything the planned demo flow needs.
- [ ] With `APP_MODE=viva` (or equivalent), the application serves the demo flow with zero live calls to GitHub/Jira/Confluence/Drive/Gemini/Groq.
- [ ] A rehearsal run of the full demo script, with network access to those external services deliberately disabled, succeeds end-to-end.

## Tests

- [ ] Unit — n/a
- [ ] Integration — n/a
- [ ] Security — n/a
- [ ] E2E — the network-disabled rehearsal run described above is the definitive test for this task

## Documentation updates

`docs/DEMO.md` — document exactly how to run this script and how to verify viva-mode has no live dependencies.

## Known limitations

_Fill in at completion._
