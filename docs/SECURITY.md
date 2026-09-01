# Security Architecture

Security is cross-cutting.

## Identity
- session/token controls (HMAC-SHA256 JWT tokens using `JWT_SECRET_KEY` from `core/config.py`),
- MFA extension point (`mfa_verified: bool`, `amr: ["pwd", "mfa"]` claims in JWT tokens),
- Local password auth (bcrypt) for dev/demo mode alongside enterprise OIDC/SAML provider integration paths,
- Internal identity mapping (`User.id` internal UUID with `external_identity_provider` and `external_identity_id`).

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
