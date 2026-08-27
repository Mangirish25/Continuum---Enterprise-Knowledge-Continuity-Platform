# Task System

Tasks are implementation slices, not architecture documents.

## Task format

Each task must contain:

```text
ID
Title
Status
Priority
Depends on
Requirements
Goal
Scope
Out of scope
Implementation notes
Acceptance criteria
Tests
Documentation updates
Known limitations
```

## Rules

- One task should produce a coherent vertical slice.
- Dependencies must be checked before implementation.
- Acceptance criteria must be testable.
- Tasks should reference requirement IDs.
- Completed tasks are historical records; do not rewrite them to hide changes.
- If implementation discovers an architecture conflict, update an ADR instead of silently drifting.

## Suggested implementation order

1. Foundation + project scaffolding
2. Database + migrations
3. Identity + organization authorization
4. Projects/assets/ownership
5. Audit ledger
6. Frontend shell
7. One connector end-to-end
8. Knowledge/RAG
9. KCS + bus factor
10. Handover workflow
11. Succession recommendation
12. Controlled ownership/access workflow
13. Coordinator and supporting agents
14. Notifications
15. Reliability/security hardening
16. Additional connectors
17. Demo hardening
