# Task 017 — `apps/web/src/api/client.ts`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 001/002 (Dockerfiles — needs an agreed API base URL convention), effectively unblocked once Task 010 (auth API) exists to call against
**Requirements:** supports REQ-P001 (dashboards/UI for projects, employees, knowledge, handover) across all later frontend features
**Board ref:** `tasks/BOARD.md` — Phase 6.1
**Owner:** Rahul

## Goal

A single typed HTTP client every frontend feature imports, instead of each feature calling `fetch`/`axios` independently with its own auth and error handling.

## Scope

- `apps/web/src/api/client.ts` — base client wrapping fetch/axios, reading the API base URL from a build/runtime env var (coordinate the exact variable name with Task 002's web Dockerfile).
- Attaches the auth token (once Task 019 — `useAuth.ts` — exists) to every request automatically.
- Centralized error handling: a failed request surfaces a typed client-side error shape (status code, server error code/message from Task 006's backend error format) rather than letting each component parse raw responses differently.
- A 401 response triggers a single, consistent handling path (e.g. token refresh attempt, then redirect to login) rather than each feature reacting independently.

## Out of scope

- Per-endpoint typed request/response functions for specific features (projects, assets, etc.) — those live in each feature's own API module and call this client, not the other way around.
- Retry/offline queuing logic — not required for the current phase; note as a future improvement if skipped.

## Implementation notes

- This file is imported almost everywhere in the frontend — keep its public surface small and stable; changing its shape later forces a ripple edit across every feature.
- Can be built and tested against a mocked/stubbed backend if Task 010 isn't finished yet (`docs/DEMO.md`'s 'use synthetic data early to avoid being blocked by teammates' incomplete work' principle applies to local dev too, not just the viva).

## Acceptance criteria

- [ ] A request made through the client automatically includes the auth token when one is available.
- [ ] A failed request (4xx/5xx) surfaces a consistent, typed error object to the caller.
- [ ] A 401 triggers one defined, consistent handling path.
- [ ] The API base URL is configurable per environment, not hardcoded.

## Tests

- [ ] Unit — client correctly attaches auth header, correctly parses success/error responses
- [ ] Integration — a real request against a running backend (Task 010) succeeds and a 401 is handled as designed
- [ ] Security — confirm the auth token is never logged or exposed in client-visible error messages
- [ ] E2E — n/a yet

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
