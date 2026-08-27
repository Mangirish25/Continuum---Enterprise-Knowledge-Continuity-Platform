# Enterprise Knowledge Continuity Platform (EKCP)

## Purpose

EKCP is an enterprise knowledge-continuity platform designed around one business problem:

> Critical knowledge, ownership context, and operational responsibility can disappear when employees leave.

The platform connects enterprise knowledge sources, normalizes and indexes their information, identifies continuity risks, supports permission-aware knowledge retrieval, prepares controlled handovers, recommends successors with human approval, and records important changes in a tamper-evident audit history.

## Four systems

1. **Knowledge System** — What information exists, where it is, and who may see it?
2. **Continuity/Risk System** — What knowledge or ownership is at risk?
3. **Handover/Workflow System** — How do we transfer responsibility safely and verify completion?
4. **Audit/Security System** — Who did what, when, under what authorization, and can tampering be detected?

## Start here

For humans:
1. `docs/PROJECT.md`
2. `docs/GLOSSARY.md`
3. `docs/REQUIREMENTS.md`
4. `docs/ARCHITECTURE.md`

For Codex:
1. `AGENTS.md`
2. `docs/REQUIREMENTS.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DECISIONS.md`
5. The relevant task in `tasks/`

## Documentation authority

The repository is documentation-first. `AGENTS.md` defines coding-agent rules. Product and architecture decisions are maintained under `docs/`.

When documents conflict, follow the precedence defined in `AGENTS.md`.

## Current implementation status

The documentation describes the target architecture. Do not interpret a documented component as implemented unless the repository code and task history confirm it.

`docs/DECISIONS.md` carries a decision-status table (`ACCEPTED` / `PROPOSED` / `IMPLEMENTATION DETAIL` / `NOT REQUIRED` / `OUT OF SCOPE`) — check it before assuming a named technology, framework, or connector is either locked in or in scope.

Implemented so far: GitHub connector (`github_connector.py`), Gemini rate limiter (`gemini_rate_limiter.py`), Gemini client (`gemini_client.py`).

## Core implementation direction

- Modular monolith for the initial application.
- Asynchronous workers for long-running work.
- PostgreSQL as the structured system of record.
- Object storage for large files/assets.
- Rebuildable vector index for semantic retrieval.
- Permission-aware retrieval; vector search is not the authorization layer.
- AI behind explicit tool/policy boundaries.
- Human approval for sensitive actions.
- Tamper-evident audit ledger with controlled writes and optional external immutable checkpointing.
- Source systems remain authoritative for source-owned data.
