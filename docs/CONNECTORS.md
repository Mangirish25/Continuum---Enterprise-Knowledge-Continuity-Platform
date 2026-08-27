# Connector Contract

## 1. Purpose

Connectors translate external systems into a normalized internal representation. They must not contain unrelated business logic.

**API-only access (ACCEPTED, see ADR-013):** Connectors must retrieve data through supported source-system APIs only — targeted metadata/content calls, not bulk export.

```text
GitHub API                          NOT: git clone
   |                                       |
targeted metadata/content retrieval   entire repository on disk
   |                                       |
normalize                             scan everything
```

Bulk repository cloning or bulk downloading of a source system to local disk is prohibited unless an explicit ADR permits it for a specific, documented reason. The GitHub connector's use of GraphQL v4 (single round-trip query for README, issues, PR comments) plus REST v3 (file tree) is the reference implementation of this rule — new connectors should follow the same shape: smallest sufficient API surface, no local mirroring.

Initial/example providers:
- GitHub — implemented (`github_connector.py`)
- Jira
- Confluence
- Google Drive
- enterprise identity provider

Slack is **out of scope** for the current implementation. It may appear in conceptual architecture diagrams elsewhere as an example enterprise knowledge source, but should not be built unless explicitly added to the connector roadmap via an ADR. See `docs/PROJECT.md` §4.

## 2. Common interface

A connector should provide capabilities equivalent to:

```text
connect()
health_check()
list_items()
fetch_item()
get_permissions()
get_version()
sync()
```

Provider capabilities may vary; unsupported capabilities must be explicit.

## 3. Normalized objects

The ingestion layer should operate on common concepts such as:

- SourceDocument
- SourceAsset
- SourcePermission
- SourceChange
- SyncCursor

## 4. Pipeline

```text
Connector
 -> fetch
 -> normalize
 -> deduplicate/version
 -> extract ACL + metadata
 -> persist metadata
 -> extract content
 -> chunk
 -> embed
 -> index
```

## 5. Sync model

Support both:
- event/webhook-driven updates where available,
- periodic reconciliation to recover from missed events.

## 6. Webhook security

Validate:
- signature,
- schema,
- source,
- timestamp/replay protection where applicable.

## 7. Deletion and ACL changes

Source deletions and permission changes must propagate so EKCP does not retain unauthorized searchable knowledge indefinitely.

## 8. Secrets

Connector credentials are configuration/secrets, not source code. Production secrets belong in a secret-management mechanism.

## 9. Rate limits

All external calls must tolerate rate limiting, retries, timeouts and provider failures.
