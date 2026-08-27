# Handover Workflow

A handover is a state machine, not a loose status field.

## States

```text
DRAFT
  -> INITIATED
  -> ASSESSING
  -> KNOWLEDGE_COLLECTION
  -> HANDOVER_READY
  -> SUCCESSOR_REVIEW
  -> MANAGER_APPROVAL
  -> OWNERSHIP_TRANSFER
  -> ACCESS_REVOCATION
  -> VERIFICATION
  -> COMPLETED
```

Side/failure states:
- BLOCKED
- FAILED
- REJECTED
- CANCELLED

## Rules

- Invalid transitions must be rejected.
- Every transition must be attributable to an actor/system.
- Important transitions must create audit events.
- Side-effecting transitions must be retry-safe.
- External ownership/access operations must support partial-failure recovery.

## Handover contents

A handover should include:
- departing employee/team context,
- projects and responsibilities,
- assets and repositories,
- knowledge package,
- documentation gaps,
- tasks, owners and deadlines,
- successor recommendation and explanation,
- approvals,
- ownership transfers,
- access actions,
- verification results,
- linked audit/correlation IDs.

## Human approval

Sensitive actions follow:

```text
AI recommendation
 -> backend validation
 -> authorization
 -> authorized human approval
 -> executor
 -> verification
 -> audit
```

## Credential lifecycle

Never transfer a person's personal credentials.

For service accounts:
- identify secret,
- rotate it through the approved secret-management path,
- update authorized consumers,
- verify,
- revoke the old credential,
- audit the lifecycle.

For personal accounts:
- revoke old access,
- provision the new authorized identity,
- audit.
