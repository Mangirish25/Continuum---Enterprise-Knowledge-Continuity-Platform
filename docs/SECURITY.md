# Security Architecture

Security is cross-cutting.

## Identity
- session/token controls,
- MFA where applicable,
- OIDC/SAML integration path for enterprise identity,
- internal identity mapping.

## Authorization
Use layered controls:
1. authenticated identity,
2. organization boundary,
3. role permissions,
4. project/resource membership,
5. classification/ACL rules,
6. PostgreSQL RLS where appropriate.

## RAG
- ACL-aware retrieval,
- source permission synchronization,
- deletion propagation,
- citations,
- prompt-injection defense,
- no LLM-based authorization.

## Files
- validate file type/size,
- classification,
- safe storage,
- encryption where appropriate,
- malware scanning where feasible.

## Secrets
- never commit secrets,
- development `.env` is acceptable for local use,
- production uses a secret-management/deployment mechanism.

## Webhooks
- signature validation,
- schema validation,
- replay protection,
- idempotent processing.

## Audit
- controlled writer permissions,
- canonical event hashing,
- serialized chain writes,
- verification endpoint,
- optional external immutable checkpoint.

## Data lifecycle
Define:
- active,
- stale,
- archived,
- deleted,
- retention/expiry behavior.

## Monitoring
Monitor:
- failed authentication,
- authorization failures,
- unusual access,
- integration failures,
- audit verification failures,
- repeated job failures.
