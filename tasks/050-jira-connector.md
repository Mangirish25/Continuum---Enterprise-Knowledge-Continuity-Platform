# Task 050 — `apps/api/app/integrations/jira_connector.py`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 024 (ingestion worker pattern), the existing `github_connector.py` as the reference implementation
**Requirements:** REQ-P003, ADR-013 (API-only connector access)
**Board ref:** `tasks/BOARD.md` — Phase 16.1
**Owner:** Sanmati

## Goal

A Jira connector following the GitHub connector's established API-only pattern — the next connector in the roadmap per the project's stated sequence (GitHub → Jira → Confluence → Google Drive).

## Scope

- `apps/api/app/integrations/jira_connector.py`
- Atlassian API token authentication, targeted retrieval (issues, comments, relevant metadata) via Jira's REST API — no bulk export.
- Conforms to whatever connector interface `github_connector.py` and Task 024's ingestion worker expect, so it's a drop-in addition rather than requiring worker changes.

## Out of scope

- Confluence (Task 051) and Google Drive (Task 052) — separate connectors, separate tasks.
- Jira webhook support — polling/on-demand retrieval is consistent with the project's established API-only approach; revisit only if Task 049's webhook validation is actually needed here.

## Implementation notes

- Read `github_connector.py`'s actual implementation before starting — the goal is consistency with its established shape (GraphQL/REST usage pattern, error handling, rate-limit awareness, no local mirroring), not an independently-designed connector that happens to also talk to Jira.

## Acceptance criteria

- [ ] Connector authenticates via Atlassian API token and retrieves real issue/comment data via targeted API calls only — no bulk export.
- [ ] Conforms to the existing connector interface Task 024's worker expects.
- [ ] Errors (auth failure, rate limit, not-found) map to typed exceptions (Task 006), consistent with the GitHub connector's approach.

## Tests

- [ ] Unit — connector logic against a mocked Jira API
- [ ] Integration — a real call against a test Jira instance/project
- [ ] Security — confirm the API token is never logged; confirm no bulk-export code path exists
- [ ] E2E — full ingestion run (Task 024) using this connector

## Documentation updates

`docs/CONNECTORS.md` — move Jira from the provider list's unimplemented state to implemented.

## Known limitations

_Fill in at completion._
