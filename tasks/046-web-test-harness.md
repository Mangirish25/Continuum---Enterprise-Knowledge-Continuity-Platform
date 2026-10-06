# Task 046 — `apps/web/tests/`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 002 (web Dockerfile), effectively spans Phase 6+ frontend work
**Requirements:** supports verification of Phase 6+ frontend tasks
**Board ref:** `tasks/BOARD.md` — Phase 15.2
**Owner:** Paras

## Goal

A real frontend test harness (component testing + a basic E2E runner) so Phase 6+ tasks' 'Tests' sections have somewhere to live.

## Scope

- `apps/web/tests/` — component-test setup (e.g. React Testing Library or equivalent) and a basic E2E runner config (e.g. Playwright/Cypress) pointed at a real running stack.
- At least one working example test per category, so later tasks have a pattern to copy.

## Out of scope

- Writing every individual frontend task's tests — shared infra only, same boundary as Task 045.
- Visual regression testing — not required for current scope.

## Implementation notes

- Keep E2E test setup realistic about demo-stability constraints (ADR-014) — E2E tests should run against controlled/seeded data in CI, not live external APIs, mirroring the same prefetch/cache discipline the actual viva demo needs.

## Acceptance criteria

- [ ] Component test setup works with at least one real example (e.g. against Task 020's AppShell or Task 022's ProjectList).
- [ ] E2E runner is configured and can run at least one real flow (e.g. login) against a running stack.

## Tests

- [ ] Unit — n/a — this task builds the test infrastructure itself
- [ ] Integration — example tests pass against a real running stack
- [ ] Security — n/a
- [ ] E2E — the example E2E test itself is the proof this works

## Documentation updates

`docs/TESTING.md` — document frontend test conventions alongside the backend ones.

## Known limitations

_Fill in at completion._
