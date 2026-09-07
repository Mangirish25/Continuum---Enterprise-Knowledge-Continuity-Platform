# Task 012 — `apps/api/app/repositories/asset_repository.py`

**Status:** done
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

- Implemented `AssetRepository` in `apps/api/app/repositories/asset_repository.py` mirroring Task 011's pattern.
- Explicitly documented the boundary that this repository manages asset metadata rows only; file binary upload and object storage (MinIO/S3) are handled outside this repository.
- Every query enforces strict multi-tenant isolation via `organization_id`.
- Foreign entity references (`project_id`, `owner_id`) are validated to ensure they belong to the caller's organization.
- Mapped all ORM and integrity exceptions to typed exceptions (`NotFoundError`, `ConflictError`, `ValidationError`, `AppError`) from `apps/api/app/core/exceptions.py`.
- Created 15 unit, integration, and security tests in `apps/api/tests/test_asset_repository.py`. All 48 backend tests pass.

## Acceptance criteria

- [x] Full CRUD for assets, scoped to organization.
- [x] List/filter by project and by owner works correctly.
- [x] No method allows accessing an asset outside the caller's organization.
- [x] Errors map to Task 006's typed exceptions.
- [x] Repository pattern is consistent with Task 011 (same scoping mechanism, same error-handling approach).

## Tests

- [x] Unit — CRUD correctness, filtering logic
- [x] Integration — cross-organization isolation explicitly tested
- [x] Security — cross-org isolation test is mandatory
- [ ] E2E — deferred to Task 014

## Documentation updates

- None expected.

## Known limitations

- File and object storage handling (MinIO/S3 byte stream uploads and downloads) is explicitly not part of this repository. This repository manages asset metadata records only.
- Uses synchronous SQLAlchemy `Session` interface matching current session management.

