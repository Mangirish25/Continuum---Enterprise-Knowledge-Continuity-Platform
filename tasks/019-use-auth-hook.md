# Task 019 — `apps/web/src/hooks/useAuth.ts`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 017 (api client), Task 010 (auth API — needed to actually test login end-to-end, though the hook can be built against a mock first)
**Requirements:** REQ-S001 (authorization), supports every authenticated frontend feature
**Board ref:** `tasks/BOARD.md` — Phase 6.3
**Owner:** Rahul

## Goal

A single hook/context exposing current auth state (logged in/out, current user, token) and login/logout actions, so no component manages token storage independently.

## Scope

- `apps/web/src/hooks/useAuth.ts` plus a small auth context/provider if the chosen state approach needs one.
- Login/logout functions calling Task 010's endpoints via Task 017's client.
- Token storage strategy chosen deliberately (e.g. in-memory + refresh-on-load, vs. persisted) and documented here — don't default to an insecure choice (e.g. raw token in `localStorage`) without considering the tradeoff explicitly.
- Exposes current user/role info for Task 020 (AppShell) to conditionally render nav items, and for later role-gated features.

## Out of scope

- MFA UI — Task 009 only defines a backend extension point; no frontend MFA flow is required yet.
- Registration/signup UI — matches Task 010's backend scope (no self-signup in current requirements).

## Implementation notes

- This is the frontend's equivalent of Task 009/010 on the backend — treat token handling with the same care; an XSS-exposed token is a real vulnerability, not a theoretical one.
- Build against a mocked login response first if Task 010 isn't ready, per the project's 'use synthetic data early' working principle — just make sure the mock is clearly marked and removed once the real endpoint exists.

## Acceptance criteria

- [ ] Login stores auth state and makes it available to the rest of the app.
- [ ] Logout fully clears auth state (and server-side session/refresh token if Task 010's design is stateful).
- [ ] An expired/invalid token is detected and the user is returned to a logged-out state rather than the app silently failing on every request.
- [ ] Token storage approach is deliberate and documented, not a default left unexamined.

## Tests

- [ ] Unit — state transitions on login/logout/expiry
- [ ] Integration — full login flow against a real Task 010 backend
- [ ] Security — confirm token isn't exposed in a way vulnerable to XSS given the chosen storage approach
- [ ] E2E — login → authenticated request succeeds → logout → same request fails

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
