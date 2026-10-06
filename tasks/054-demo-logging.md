# Task 054 — `infra/monitoring/logging_config.py`

**Status:** backlog
**Priority:** P2
**Depends on:** none
**Requirements:** supports a clean, professional live demo
**Board ref:** `tasks/BOARD.md` — Phase 17.2
**Owner:** Paras

## Goal

Clean, readable logging configuration so anything visible during a live demo (terminal output, logs shown to the panel) looks professional rather than noisy debug output.

## Scope

- `infra/monitoring/logging_config.py`
- Structured, leveled logging across the backend, with a demo-appropriate default level (info/warning, not verbose debug) and no secret values ever logged (consistent with every earlier task's 'no secrets in logs' requirement).

## Out of scope

- Full observability/monitoring stack (metrics, tracing, dashboards) — out of scope for the current academic-project phase; clean logs are sufficient.

## Implementation notes

- Low effort, real payoff — this is the kind of detail that affects how polished the live demo feels without being architecturally significant.

## Acceptance criteria

- [ ] Logs are structured and readable at the default demo log level.
- [ ] No secret/credential values appear in any log output, across every task that logs anything.

## Tests

- [ ] Unit — n/a
- [ ] Integration — a manual review of log output during a rehearsal run
- [ ] Security — grep logs for accidentally-leaked secret patterns
- [ ] E2E — n/a

## Documentation updates

`docs/OPERATIONS.md` — note the logging configuration and demo log level.

## Known limitations

_Fill in at completion._
