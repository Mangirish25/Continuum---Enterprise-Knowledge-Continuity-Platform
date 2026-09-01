# Task 014 — `apps/api/app/api/v1/assets.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 012 (asset repository), Task 009 (auth/RBAC), Task 010 (auth API), Task 013 (projects API — follow its established pattern rather than diverging)
**Requirements:** REQ-P002, REQ-S001
**Board ref:** `tasks/BOARD.md` — Phase 4.4
**Owner:** Sanmati

## Goal

Authenticated CRUD endpoints for assets, following the exact same pattern Task 013 establishes for projects, so the API surface is consistent.

## Scope

- `apps/api/app/api/v1/assets.py`
- REST endpoints: create/list/get/update/delete asset, filter by project/owner.
- Same authentication/authorization/error-handling/schema conventions as Task 013.

## Out of scope

- Actual file upload/object-storage handling — same boundary as Task 012; this endpoint manages asset metadata, not file bytes. If a file-upload endpoint is genuinely needed at this phase, flag it as a scope question rather than silently building it in here.
- Knowledge document/chunk endpoints — Phase 8.

## Implementation notes

- Read Task 013's actual implementation before starting, not just its task file — the goal is API consistency (same auth-dependency style, same error shapes, same schema conventions), and the most reliable way to get that is to copy the working pattern rather than re-deriving it from the docs independently.

## Acceptance criteria

- [ ] Full CRUD + filtering endpoints work end-to-end against a real running stack.
- [ ] Auth/authorization enforcement matches Task 013's pattern exactly (organization scoping, role/membership checks).
- [ ] Response schemas leak no unintended fields.
- [ ] Errors return structured responses with correct status codes.

## Tests

- [ ] Unit — schema validation
- [ ] Integration — full authenticated CRUD flow
- [ ] Security — cross-organization and insufficient-role access explicitly rejected
- [ ] E2E — full flow: login → create asset under a project → verify cross-org isolation

## Documentation updates

- `docs/API.md` — document these endpoints alongside Task 013's.

## Known limitations

_Fill in at completion — explicitly note that file/object-storage upload is not covered here._
