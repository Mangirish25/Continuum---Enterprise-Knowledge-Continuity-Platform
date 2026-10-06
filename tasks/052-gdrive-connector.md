# Task 052 — `apps/api/app/integrations/gdrive_connector.py`

**Status:** backlog
**Priority:** P1
**Depends on:** none beyond the established connector pattern
**Requirements:** REQ-P003, ADR-013
**Board ref:** `tasks/BOARD.md` — Phase 16.3
**Owner:** Sanmati

## Goal

A Google Drive connector using OAuth 2.0 installed-app flow, as specified in the project's locked tech stack.

## Scope

- `apps/api/app/integrations/gdrive_connector.py`
- OAuth 2.0 installed-app authentication flow (not a service account, per the project's stated choice) and targeted document retrieval via the Google Drive API.

## Out of scope

- Google Workspace admin-level bulk export tools — API-only targeted retrieval, consistent with ADR-013, same as every other connector.

## Implementation notes

- The OAuth installed-app flow needs a credential refresh/storage strategy for a long-running backend process — work out how a token obtained via an interactive OAuth flow gets persisted and refreshed without a human re-authenticating on every run, and document the chosen approach clearly since this is less automatic than Task 050/051's API-token auth.

## Acceptance criteria

- [ ] OAuth 2.0 installed-app flow is implemented and documented.
- [ ] Token refresh works without requiring repeated manual re-authentication for routine ingestion runs.
- [ ] Document retrieval is targeted (specific files/folders), not a bulk account-wide export.

## Tests

- [ ] Unit — connector logic against a mocked Drive API
- [ ] Integration — a real call against a test Drive account/folder
- [ ] Security — confirm OAuth tokens are stored securely (not logged, not committed) and refresh correctly
- [ ] E2E — full ingestion run using this connector

## Documentation updates

`docs/CONNECTORS.md` — mark Google Drive implemented; document the OAuth token storage/refresh approach.

## Known limitations

_Fill in at completion._
