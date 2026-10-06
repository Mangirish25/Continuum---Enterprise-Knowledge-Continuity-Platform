# Task 045 — `apps/api/tests/`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 003 (compose stack, for a real test database), effectively spans everything built so far — can start early with scaffolding and grow as tasks land
**Requirements:** supports verification of every REQ/ADR already implemented
**Board ref:** `tasks/BOARD.md` — Phase 15.1
**Owner:** Paras

## Goal

A real pytest harness (fixtures, test database setup/teardown, auth helpers) so every backend task's own 'Tests' section has somewhere to actually live, rather than each task inventing its own ad hoc test setup.

## Scope

- `apps/api/tests/` — fixtures for a test database (isolated from dev data, using Task 003's compose Postgres or a dedicated test instance), an authenticated-test-client helper (building on Task 009/010), and conventions for unit vs. integration vs. security test organization.
- Retroactively wire up test files for already-completed tasks (007–044 as they land) into this harness rather than leaving them as scattered ad hoc scripts.

## Out of scope

- Writing every individual task's tests from scratch — those are each task's own responsibility per its 'Tests' section; this task provides the shared harness/fixtures they plug into.
- Frontend tests — Task 046.

## Implementation notes

- This should ideally exist early (even a minimal version) so Phase 2 onward can write real tests against it rather than everyone deferring testing to 'later.' If it's genuinely landing this late in practice, prioritize retrofitting the highest-risk already-built pieces first — Task 015's audit ledger and Task 028's permission filter are the two most important to have real automated tests for.

## Acceptance criteria

- [ ] A test database fixture exists, isolated from dev/demo data.
- [ ] An authenticated test-client helper exists so endpoint tests don't each reimplement login.
- [ ] Existing completed tasks' test plans can be executed against this harness.
- [ ] CI (Task 048) can run this harness non-interactively.

## Tests

- [ ] Unit — n/a — this task builds the test infrastructure itself
- [ ] Integration — the harness itself runs cleanly against a fresh test database
- [ ] Security — confirm test runs never touch dev/demo/production data
- [ ] E2E — n/a

## Documentation updates

`docs/TESTING.md` — document how to run tests locally and what the fixture/helper conventions are.

## Known limitations

_Fill in at completion._
