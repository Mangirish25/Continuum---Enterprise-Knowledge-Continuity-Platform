# Task 027 — `apps/api/app/rag/hybrid_retrieval.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 026 (embeddings)
**Requirements:** REQ-A001, ADR-012
**Board ref:** `tasks/BOARD.md` — Phase 8.5
**Owner:** Mangirish

## Goal

Hybrid retrieval combining BM25 lexical search and ChromaDB dense vector search via Reciprocal Rank Fusion, exactly as ADR-012 specifies — this is what the Knowledge Assistant (Task 029) and the agents (Phase 11/13) actually query.

## Scope

- `apps/api/app/rag/hybrid_retrieval.py`
- BM25 lexical search over chunk text (can be a standard BM25 implementation over chunk content, indexed however is simplest given the current stack — doesn't need its own separate service unless chunk volume demands it).
- Dense vector search against ChromaDB (Task 026's output).
- Reciprocal Rank Fusion to combine both result sets into a single ranked list, per ADR-012.
- Returns results with enough metadata (source document, chunk, score) for Task 028's permission filter to apply, and for the Knowledge Assistant to cite sources.

## Out of scope

- Permission-aware filtering — Task 028, which wraps this task's output.
- Query rewriting/expansion — a reasonable first version does plain hybrid search on the user's query as given; query enhancement is a future refinement, not required now.

## Implementation notes

- This is the retrieval core the whole Knowledge Assistant depends on — get the RRF fusion logic correct and testable in isolation (given known BM25 and vector result lists, confirm the fused ranking is as expected) rather than only testing it end-to-end where ranking bugs are hard to spot.

## Acceptance criteria

- [ ] Given a query, returns a fused, ranked result set combining BM25 and vector search.
- [ ] RRF fusion logic is independently correct given known inputs (not just 'looks reasonable' on real data).
- [ ] Results carry enough metadata (source, chunk id, score) for downstream permission filtering and citation.

## Tests

- [ ] Unit — RRF fusion logic against known BM25/vector result lists with a hand-computed expected ranking
- [ ] Integration — full retrieval against a real ChromaDB + chunk corpus from Tasks 024–026
- [ ] Security — n/a — permission filtering is Task 028's responsibility, not this task's
- [ ] E2E — n/a yet

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
