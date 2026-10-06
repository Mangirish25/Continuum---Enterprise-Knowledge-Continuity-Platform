# Task 055 — `apps/web/src/features/admin/AdminPanel.tsx`

**Status:** backlog
**Priority:** P2
**Depends on:** Task 009 (roles/RBAC), Task 010 (auth)
**Requirements:** REQ-P001 (admin interfaces)
**Board ref:** `tasks/BOARD.md` — Phase 17.3
**Owner:** Rahul

## Goal

A basic admin interface for organization/role management — the last frontend feature on the board.

## Scope

- `apps/web/src/features/admin/AdminPanel.tsx`
- View/manage users and their roles within the organization, gated to admin-role users only (both server-side via Task 009's RBAC, and hidden from Task 020's nav for non-admins).

## Out of scope

- Organization-creation/multi-tenant management UI — single-organization admin scope is sufficient for the current phase.

## Implementation notes

- Lower priority than the core demo-path features — reasonable to build last, consistent with its board position.

## Acceptance criteria

- [ ] Admin users can view and manage user roles within their organization.
- [ ] Non-admin users cannot reach this page's functionality, enforced server-side (not just hidden client-side).

## Tests

- [ ] Unit — component renders given sample data and role states
- [ ] Integration — role management actions against a real backend
- [ ] Security — a non-admin user's attempt to access admin actions is rejected server-side
- [ ] E2E — admin login → manage a user's role → change reflected

## Documentation updates

None expected.

## Known limitations

_Fill in at completion._
