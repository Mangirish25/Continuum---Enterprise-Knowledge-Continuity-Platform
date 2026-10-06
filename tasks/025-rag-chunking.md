# Task 025 — `apps/api/app/rag/chunking.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 024 (ingestion worker — needs normalized source content to chunk)
**Requirements:** REQ-A001 (index and search enterprise knowledge), `docs/DATABASE.md` §6
**Board ref:** `tasks/BOARD.md` — Phase 8.3
**Owner:** Mangirish

## Goal

Deterministic text chunking of ingested documents into `knowledge_chunks`, with the chunking strategy/version recorded so retrieval quality can be tracked and reproduced.

## Scope

- `apps/api/app/rag/chunking.py`
- A chunking strategy (e.g. recursive/semantic splitting with overlap) applied to `knowledge_documents` content, producing `knowledge_chunks` rows per `docs/DATABASE.md` §6's metadata requirements (parser/chunking version recorded on each chunk).
- Handles at minimum the content types the GitHub connector actually produces (README, issue/PR text, code comments if in scope) — don't over-build for document types nothing ingests yet.

## Out of scope

- Embedding generation — Task 026, which consumes this task's output.
- Chunking strategy tuning/evaluation — Task 056 (evaluation set) is where retrieval quality gets measured; this task just needs a reasonable, documented, versioned strategy, not a tuned one.

## Implementation notes

- Record the chunking strategy version on every chunk (`docs/DATABASE.md` §6) from day one — re-chunking with a changed strategy later needs to be distinguishable from the original pass, or evaluation (Task 056) can't tell what it's actually measuring.

## Acceptance criteria

- [ ] Chunks are produced deterministically from a given document and chunking-version configuration (same input, same version → same output).
- [ ] Every chunk records which document it came from and the chunking strategy/version used.
- [ ] Chunk size/overlap choices are documented, not arbitrary magic numbers with no rationale.

## Tests

- [ ] Unit — chunking produces expected boundaries for representative sample content
- [ ] Integration — chunking a real GitHub-sourced document end-to-end populates `knowledge_chunks` correctly
- [ ] Security — n/a
- [ ] E2E — n/a yet

## Documentation updates

None expected unless the chunking strategy needs documenting beyond `docs/DATABASE.md`'s existing metadata fields.

## Known limitations

_Fill in at completion._
