# Task 051 — `apps/api/app/integrations/confluence_connector.py`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 050 (Jira connector — often shares Atlassian auth plumbing)
**Requirements:** REQ-P003, ADR-013
**Board ref:** `tasks/BOARD.md` — Phase 16.2
**Owner:** Sanmati

## Goal

A Confluence connector, likely sharing Atlassian authentication with Task 050.

## Scope

- `apps/api/app/integrations/confluence_connector.py`
- Targeted retrieval of pages/spaces relevant to tracked projects, via Confluence's REST API only.

## Out of scope

- Google Drive — Task 052.

## Implementation notes

- Check whether Atlassian authentication can be shared/reused from Task 050 rather than reimplemented — if Jira and Confluence share a tenant/token in the team's actual setup, factor that out rather than duplicating it.

## Acceptance criteria

- [ ] Connector retrieves real page content via targeted API calls only.
- [ ] Shares authentication plumbing with Task 050 where applicable, rather than duplicating it.

## Tests

- [ ] Unit — connector logic against a mocked Confluence API
- [ ] Integration — a real call against a test Confluence space
- [ ] Security — confirm no bulk-export code path exists
- [ ] E2E — full ingestion run using this connector

## Documentation updates

`docs/CONNECTORS.md` — mark Confluence implemented.

## Known limitations

_Fill in at completion._
