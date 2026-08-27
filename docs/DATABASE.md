# Database Contract

## 1. System of record

PostgreSQL is the primary structured system of record.

## 2. Core tables

At minimum:

- organizations
- departments
- teams
- users
- roles
- user_roles
- skills
- user_skills
- projects
- project_members
- project_dependencies
- assets
- knowledge_documents
- knowledge_chunks
- integrations
- external_objects
- sync_runs
- handovers
- handover_tasks
- handover_approvals
- ownership_transfers
- access_actions
- risk_assessments
- notifications
- audit_events
- audit_verifications

## 3. Tenant boundary

Every tenant-owned entity must carry `organization_id` directly or through a guaranteed organization-scoped relationship.

Authorization must be applied at the application layer and, where appropriate, PostgreSQL RLS.

## 4. External identity

Use internal user IDs while preserving external identity/provider IDs for integrations.

## 5. External object uniqueness

External objects must be uniquely identified by the integration/provider plus external identifier/version rules.

## 6. Knowledge metadata

Knowledge documents/chunks should preserve enough metadata for authorization and rebuildability, including:

- organization_id
- project_id where applicable
- source_type
- source_url/reference
- source_version
- checksum
- classification
- owner_id
- allowed roles/groups/users as applicable
- ACL version
- parser version
- chunking version
- embedding model/version
- timestamps

## 7. Constraints

Use:
- foreign keys,
- unique constraints,
- check constraints,
- indexes,
- explicit nullability,
- deletion policies,
- transaction boundaries.

## 8. Audit model

An audit event includes:

```text
event_id
sequence
organization_id
timestamp
actor_type
actor_id
action_type
entity_type
entity_id
old_state_hash
new_state_hash
request_id
correlation_id
metadata
previous_hash
current_hash
```

`current_hash = SHA256(previous_hash || canonical_event)`

Audit chain writes must be serialized/controlled so concurrent writers cannot create conflicting predecessors.

## 9. Migrations

Every schema change requires a migration. Never modify production-like schema manually as the normal workflow.
