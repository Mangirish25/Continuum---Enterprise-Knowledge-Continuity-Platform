# Task 026 — `apps/api/app/rag/embeddings.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 025 (chunking)
**Requirements:** REQ-A001, ADR-012 (ChromaDB as vector store)
**Board ref:** `tasks/BOARD.md` — Phase 8.4
**Owner:** Mangirish

## Goal

Generate and store embeddings for every chunk, feeding ChromaDB (ADR-012) as the vector index, with the embedding model/version recorded per chunk.

## Scope

- `apps/api/app/rag/embeddings.py`
- Embedding generation using the project's chosen embedding approach (sentence-transformers, per the project's current tech usage) — confirm the specific model against whatever the team has already settled on, rather than picking a new one silently.
- Writes resulting vectors into ChromaDB, with the embedding model/version recorded on the corresponding `knowledge_chunks` row (`docs/DATABASE.md` §6) so ChromaDB's contents remain provably rebuildable from Postgres + object storage, per ADR-012 ('ChromaDB is derived state and must be rebuildable').

## Out of scope

- Hybrid retrieval/RRF fusion logic — Task 027 consumes this task's output.
- Re-embedding/migration tooling for a future model change — note as a future need, not required now.

## Implementation notes

- ADR-012 is explicit that ChromaDB holds derived, rebuildable state only — this module should be written so that, given Postgres + object storage, it could regenerate ChromaDB's contents from scratch if the vector store were wiped. Don't let any irreplaceable state end up only in ChromaDB.
- Respect the Gemini rate limiter if any embedding step routes through the Gemini-backed LLM Gateway — if a separate local/sentence-transformers model is used instead (as implied by the project's current stack), this task likely has no Gemini rate-limit exposure at all; confirm which applies before assuming either way.

## Acceptance criteria

- [ ] Every chunk from Task 025 gets an embedding stored in ChromaDB.
- [ ] Embedding model/version is recorded per chunk in Postgres.
- [ ] Given a cleared ChromaDB instance, re-running this module against existing chunks fully reconstructs the vector index.

## Tests

- [ ] Unit — embedding generation produces expected-shape vectors for sample input
- [ ] Integration — full pipeline (Task 024 → 025 → 026) against a real ChromaDB instance
- [ ] Security — n/a
- [ ] E2E — n/a yet

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
