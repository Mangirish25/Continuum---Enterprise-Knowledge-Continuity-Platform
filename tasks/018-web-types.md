# Task 018 — `apps/web/src/types/index.ts`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 007 (ORM models) and Task 013/014 (API schemas) for the shapes to mirror — can start from the documented shapes in `docs/API.md`/`docs/DATABASE.md` and adjust once those land
**Requirements:** supports all Phase 6+ frontend features; keeps frontend/backend contract explicit
**Board ref:** `tasks/BOARD.md` — Phase 6.2
**Owner:** Rahul

## Goal

Shared TypeScript types matching the backend's actual request/response schemas, so every feature works against one source of truth instead of ad hoc inline types.

## Scope

- `apps/web/src/types/index.ts` (or a small set of files re-exported from here, organized by domain — project, asset, user, handover, risk — per `docs/IMPLEMENTATION_STRUCTURE.md`).
- Types for every entity the frontend will render in Phase 6–17: User, Project, Asset, Handover, RiskAssessment, Notification, and their request/response wrapper shapes.
- Kept in sync with the backend's Pydantic schemas as each backend task lands — this file should be revisited, not left stale, as Tasks 013/014/033/034 etc. are completed.

## Out of scope

- Auto-generated types from an OpenAPI spec — nice-to-have, not required for this phase; if `docs/API.md` ends up precise enough to generate from later, that's a follow-up, not blocking now.
- Runtime validation (e.g. zod schemas) — these are compile-time types only unless a later task specifically asks for runtime validation.

## Implementation notes

- Treat drift between this file and the real backend response shape as a bug, not a documentation nicety — a stale type silently defeats the whole purpose of using TypeScript here.
- Where the backend isn't built yet, derive types from `docs/DATABASE.md`'s field lists and `docs/API.md`'s documented contract rather than guessing.

## Acceptance criteria

- [ ] Core entity types exist for every table/feature Phase 6 needs to render.
- [ ] Types are organized by domain, not one giant undifferentiated file.
- [ ] No `any` used where the actual shape is knowable from the docs.

## Tests

- [ ] Unit — n/a — type-only file; correctness is enforced by the TypeScript compiler across consuming code
- [ ] Integration — n/a
- [ ] Security — n/a
- [ ] E2E — n/a

## Documentation updates

Flag to Sanmati/Mangirish if a documented schema in `docs/API.md` doesn't match what their endpoint actually returns.

## Known limitations

_Fill in at completion._
