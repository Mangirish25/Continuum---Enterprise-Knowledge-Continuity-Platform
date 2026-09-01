# Task 012 — `apps/api/app/repositories/asset_repository.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 007 (ORM models), Task 008 (initial migration)
**Requirements:** REQ-P002 (track users, projects, assets, ownership and continuity metadata), REQ-S001 (server-side authorization)
**Board ref:** `tasks/BOARD.md` — Phase 4.2
**Owner:** Sanmati

## Goal

The data-access layer for assets — mirrors Task 011's pattern for `assets`, so the two repositories are consistent rather than independently reinvented.

## Scope

- `apps/api/app/repositories/asset_repository.py`
- CRUD operations against `assets` (create, get, list, update, delete per Task 007's documented policy).
- Filtering/listing by project, by owner, and by organization.
- Every query scoped by `organization_id`, following the exact same enforcement pattern Task 011 established — do not invent a different scoping approach for this repository.

## Out of scope

- `knowledge_documents`/`knowledge_chunks` — those belong to the RAG pipeline (Phase 8) and get their own repository/access pattern there, even though they're conceptually related to assets. Don't fold them into this task.
- File upload/storage handling (MinIO/S3 interaction) — this repository manages asset *metadata* rows; actual file bytes and object-storage interaction are a separate concern, likely introduced alongside whichever task first needs to store a real file. Note this boundary explicitly in the code so it's clear this repository doesn't touch object storage.
- Classification/ACL enforcement beyond organization scoping — `docs/DATABASE.md` §6 lists `classification` and ACL fields for knowledge documents specifically; for plain `assets` rows, only organization-level scoping is required at this phase unless Task 007's schema says otherwise.

## Implementation notes

- Follow Task 011's repository pattern exactly (organization-scoping mechanism, error mapping to Task 006's exceptions, NotFound-vs-Forbidden non-leakage). If Task 011 finishes first, read its actual implementation rather than just this task file's description before starting.
- If `assets` and `knowledge_documents` end up looking suspiciously similar once Phase 8 arrives, that's expected — resist the urge to merge them prematurely now; that's an architecture decision for whoever picks up Phase 8, not something to pre-empt here.

## Acceptance criteria

- [ ] Full CRUD for assets, scoped to organization.
- [ ] List/filter by project and by owner works correctly.
- [ ] No method allows accessing an asset outside the caller's organization.
- [ ] Errors map to Task 006's typed exceptions.
- [ ] Repository pattern is consistent with Task 011 (same scoping mechanism, same error-handling approach).

## Tests

- [ ] Unit — CRUD correctness, filtering logic
- [ ] Integration — cross-organization isolation explicitly tested
- [ ] Security — cross-org isolation test is mandatory
- [ ] E2E — deferred to Task 014

## Documentation updates

- None expected.

## Known limitations

_Fill in at completion — note explicitly that file/object-storage handling is not part of this repository, so nobody assumes it's covered._
