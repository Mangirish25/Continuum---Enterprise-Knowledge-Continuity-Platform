# Task 024 — `apps/api/app/workers/ingestion_worker.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 007/008 (DB), Task 015 (audit ledger — ingestion is a state change worth recording), the already-implemented `github_connector.py`
**Requirements:** REQ-P003 (discover/collect knowledge from connected systems), ADR-013 (API-only connector access)
**Board ref:** `tasks/BOARD.md` — Phase 7.2
**Owner:** Sanmati

## Goal

The async job that takes a connector's output (starting with the existing GitHub connector) and lands it as normalized `external_objects`/`sync_runs` rows — the pipeline Phase 8's RAG ingestion will build on top of.

## Scope

- `apps/api/app/workers/ingestion_worker.py`
- Runs a connector (GitHub first), writes results into `external_objects` and records a `sync_runs` row (per `docs/DATABASE.md` §5) with status/timing/error info.
- Retries/timeouts on connector calls, consistent with `AGENTS.md`'s reliability rule that external integrations must tolerate timeouts and failures gracefully.
- Failures are recorded (not silently swallowed) so a bad sync is visible, not just missing.

## Out of scope

- Jira/Confluence/Google Drive connectors themselves — Phase 16 (Tasks 050–052); this worker should be written generically enough to run any connector matching the established interface, but only GitHub needs to actually work end-to-end now.
- Triggering/scheduling strategy (cron vs. on-demand vs. webhook-triggered) beyond making the worker callable — pick the simplest that works for now and note the choice.

## Implementation notes

- This is the first consumer of the GitHub connector beyond the connector itself — treat any friction here as a signal about the connector's interface, and flag it rather than working around it with worker-side hacks.
- Respects ADR-013 — this worker should call the connector's existing API-only methods, never fall back to any kind of local clone/bulk download itself.

## Acceptance criteria

- [ ] Running this worker against a real (or test) GitHub source populates `external_objects` and a `sync_runs` row correctly.
- [ ] A connector failure (timeout, auth error, rate limit) is caught, recorded in `sync_runs` with a clear error, and does not crash the worker process.
- [ ] Re-running the worker doesn't duplicate already-ingested objects (confirm the uniqueness behavior `docs/DATABASE.md` §5 expects).

## Tests

- [ ] Unit — worker logic against a mocked connector (success and failure cases)
- [ ] Integration — real run against the GitHub connector and a real Postgres instance
- [ ] Security — confirm no secrets/tokens leak into `sync_runs` error messages or logs
- [ ] E2E — n/a — Phase 8 provides the first real downstream consumer

## Documentation updates

`docs/CONNECTORS.md` — note the ingestion worker as the standard way a connector's output reaches the database, if not already implied.

## Known limitations

_Fill in at completion._
