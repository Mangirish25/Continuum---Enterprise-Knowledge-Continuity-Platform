# Task 048 — `.github/workflows/ci.yml`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 045 (backend tests), Task 046 (frontend tests), Task 001/002 (Dockerfiles, for a build step)
**Requirements:** supports reliable verification of every task's acceptance criteria going forward
**Board ref:** `tasks/BOARD.md` — Phase 15.4
**Owner:** Paras

## Goal

A CI pipeline that runs lint, tests (including Task 047's rate-limiter load test), and builds on every change — the automated backstop behind every task's 'Tests' checklist.

## Scope

- `.github/workflows/ci.yml` (or equivalent for whatever CI platform the team actually uses).
- Lint (backend + frontend), Task 045's backend test suite, Task 046's frontend test suite, Task 047's rate-limit load test specifically called out as a required check, and a build step for Task 001/002's Dockerfiles.
- Fails the pipeline clearly and specifically (not just 'something failed') so a teammate can tell at a glance which task's acceptance criteria broke.

## Out of scope

- Continuous deployment — CI (verification) only, not CD (deployment) for the current phase.
- Secrets management in CI beyond what's needed to run tests — don't wire real production credentials into CI; use test-safe values consistent with Task 004's `.env.example` pattern.

## Implementation notes

- This is the point where all of Phase 1–14's individual task discipline becomes enforced automatically rather than relying on every teammate remembering to run tests locally before pushing.

## Acceptance criteria

- [ ] Pipeline runs lint, backend tests, frontend tests, and a Docker build on every push/PR.
- [ ] Task 047's rate-limiter load test is a required, visible check, not bundled anonymously into a generic test step.
- [ ] A failing step clearly identifies what failed.
- [ ] No real secrets are used in or exposed by the CI configuration.

## Tests

- [ ] Unit — n/a
- [ ] Integration — the pipeline itself running successfully on a real PR is the test
- [ ] Security — confirm no secret values are logged or exposed in CI output
- [ ] E2E — n/a

## Documentation updates

`docs/OPERATIONS.md` — document the CI pipeline and what a failure means for each check.

## Known limitations

_Fill in at completion._
