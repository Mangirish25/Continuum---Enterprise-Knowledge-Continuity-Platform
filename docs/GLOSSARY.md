# Glossary

**Asset** — A continuity-tracked repository, document, resource, or other enterprise item.

**Knowledge Document** — Normalized source content associated with an asset and version.

**Knowledge Chunk** — A retrieval-sized portion of a document with metadata and embedding information.

**RAG** — Retrieval-Augmented Generation: retrieve authorized source content and provide it to an LLM for grounded generation.

**ACL** — Access-control metadata originating from the source system.

**RBAC** — Role-Based Access Control.

**RLS** — PostgreSQL Row-Level Security used as a defense-in-depth data boundary.

**KCS** — Knowledge Continuity Score, an explainable continuity metric.

**Bus Factor** — A measure of how concentrated critical knowledge/responsibility is among too few people.

**Handover** — The controlled workflow for transferring responsibility and knowledge when a person leaves or changes role.

**Policy Gate** — Backend authorization/policy step that decides whether a requested tool action is allowed.

**Agent** — An AI component that reasons within a defined responsibility and may request approved tools.

**Tool** — A bounded callable capability exposed to an agent.

**Executor** — Backend component that performs an approved side effect.

**Audit Event** — A structured record of an important business/security action.

**Tamper-evident** — Later unauthorized modification should be detectable; it does not mean physical immutability.

**Source of truth** — System authoritative for a particular class of information.

**Idempotency** — Repeating the same request does not repeat its intended side effect.

**Checkpoint** — An independent integrity anchor for a range of audit events.

**WORM** — Write Once Read Many immutable storage concept.

**Correlation ID** — Identifier connecting related operations across API requests, workers, integrations and audit events.

**LLM Gateway** — The internal boundary all application code must call through to reach an LLM provider (Gemini, Groq, or LiteLLM fallback), rather than calling a provider SDK directly. Enforces the Gemini rate limiter.

**Decision status** — The lifecycle label (`ACCEPTED`, `PROPOSED`, `IMPLEMENTATION DETAIL`, `NOT REQUIRED`, `OUT OF SCOPE`) attached to each entry in `docs/DECISIONS.md`, telling a coding agent whether a technology or design choice may be changed without architectural review.

**Viva/demo mode** — The constrained runtime mode used during the live defense, in which live external dependencies are prohibited and all required data/AI outputs must be prefetched or cached (ADR-014). Distinct from development integration mode, where live APIs are allowed.
