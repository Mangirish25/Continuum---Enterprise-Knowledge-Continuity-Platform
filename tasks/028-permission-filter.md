# Task 028 — `apps/api/app/rag/permission_filter.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 027 (hybrid retrieval), Task 009 (RBAC — needs a way to check what a user can access)
**Requirements:** REQ-S002 (permission-aware retrieval — a user must not receive a document merely because it's semantically relevant; it must also be accessible to them)
**Board ref:** `tasks/BOARD.md` — Phase 8.6
**Owner:** Mangirish

## Goal

Enforce the Guide's key enterprise requirement explicitly: wrap Task 027's retrieval so results are filtered to what the requesting user is actually authorized to see, not just what's semantically relevant.

## Scope

- `apps/api/app/rag/permission_filter.py`
- Given Task 027's ranked results and the requesting user's identity/org/role (from Task 009), filters out any chunk whose source document the user isn't authorized to access (per `docs/DATABASE.md` §6's classification/ACL fields on `knowledge_documents`).
- Filtering happens server-side, before results ever reach an LLM prompt or the client — never rely on the LLM or frontend to enforce this (`docs/AI.md`: 'the LLM is never an authorization component').

## Out of scope

- Row-Level Security (RLS) implementation at the database level — this task can filter at the application layer; whether RLS is added later as defense-in-depth is a separate decision, noted but not required here.
- UI messaging about why a result was filtered — the filtering itself is silent/structural, not something the end user needs an explanation for.

## Implementation notes

- This is the single most security-critical file in the RAG pipeline — a bug here means a user could see knowledge they're not authorized for, which directly undermines the platform's whole value proposition (it manages sensitive organizational knowledge). Treat its tests with the same seriousness as Task 015's audit ledger tests.
- `docs/SECURITY.md`'s classification/ACL layer is exactly what this task enforces — read that section's exact field list before implementing the filter logic, rather than inventing a different authorization model.

## Acceptance criteria

- [ ] A user never receives a chunk from a document they're not authorized to access, regardless of semantic relevance.
- [ ] Filtering happens before any LLM call — confirm no unfiltered content is ever passed to the LLM Gateway.
- [ ] A user with full access to a document set sees the same ranking Task 027 would have produced unfiltered (i.e. filtering doesn't distort results for authorized users).

## Tests

- [ ] Unit — filter logic against synthetic documents with varied classification/ACL states and varied user permission levels
- [ ] Integration — a real retrieval run where a user is deliberately missing access to some matched documents, confirming those are excluded
- [ ] Security — this entire task is a security control — the cross-permission exclusion test above is mandatory, not optional, and should be treated as a release-blocking test
- [ ] E2E — deferred to Task 029 (Knowledge Assistant), which is the first real consumer

## Documentation updates

`docs/SECURITY.md` — confirm the implemented filtering logic matches what's documented; update if implementation revealed a gap in the documented ACL model.

## Known limitations

_Fill in at completion._
