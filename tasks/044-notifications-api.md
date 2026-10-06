# Task 044 — `apps/api/app/api/v1/notifications.py`

**Status:** backlog
**Priority:** P2
**Depends on:** Task 007 (`notifications` model), Task 043 (reminder content, though this endpoint can also support non-AI-generated notifications)
**Requirements:** REQ-P006 (deadlines, reminders, escalation, handover status updates)
**Board ref:** `tasks/BOARD.md` — Phase 14.2
**Owner:** Sanmati

## Goal

CRUD/list endpoints for notifications, following the established authenticated-endpoint pattern from Task 013.

## Scope

- `apps/api/app/api/v1/notifications.py`
- List/mark-read endpoints for a user's notifications, and an internal path for Task 043's reminder agent (or any other backend process) to create one.

## Out of scope

- Email/external delivery channels — in-app notification records are the current scope; external delivery is a future enhancement if needed.

## Implementation notes

- Follow Task 013's established pattern for auth/error/schema conventions.

## Acceptance criteria

- [ ] A user can list and mark their own notifications read/unread, scoped correctly to their organization/identity.
- [ ] An internal process (e.g. Task 043's output) can create a notification record.

## Tests

- [ ] Unit — schema validation
- [ ] Integration — full list/create/mark-read flow against a real stack
- [ ] Security — a user cannot read or modify another user's notifications
- [ ] E2E — reminder agent output → notification created → user sees it

## Documentation updates

`docs/API.md` — document these endpoints.

## Known limitations

_Fill in at completion._
