# Project Specification

## 1. Problem

Enterprise knowledge is distributed across repositories, documents, tickets, systems, and employee experience. When a critical employee leaves, organizations can lose knowledge, ownership context, and operational continuity.

## 2. Product

EKCP preserves, understands, assesses, and transfers organizational knowledge and responsibility.

## 3. Core flow

Enterprise systems
-> connectors
-> normalized knowledge/assets
-> authorization-aware indexing
-> retrieval and analysis
-> continuity/risk assessment
-> handover workflow
-> successor recommendation
-> human approval
-> controlled ownership/access actions
-> verification
-> audit

## 4. What the platform is not

- Not a replacement for GitHub, Jira, Drive, Confluence, or the enterprise IdP.
- Not a general-purpose chatbot.
- Not an autonomous HR decision-maker.
- Not a blockchain system.
- Not an unrestricted agent that can execute privileged actions.
- Not a permanent unauthorized copy of source-system data.

### Scope note: Slack

The reference Guide's architecture diagrams include Slack as an illustrative enterprise knowledge source alongside GitHub, Google Drive, and Jira. Slack integration is **out of scope** for the current implementation. The actual connector roadmap is GitHub → Jira → Confluence → Google Drive (see `docs/DECISIONS.md` decision table). Diagrams elsewhere showing Slack should be read as conceptual, not as a scope commitment — do not build a Slack connector on the basis of a diagram alone.

## 5. Primary modules

- Identity and organization management
- Projects and assets
- Knowledge ingestion and retrieval
- Continuity/risk analytics
- Handover management
- Succession recommendations
- Integrations
- Notifications
- Audit and governance

## 6. Source-of-truth rules

| Information | Authoritative source | EKCP role |
|---|---|---|
| Employee identity | Enterprise IdP | Reference/cache + authorization context |
| Source code | Source repository | Index metadata/content for continuity |
| Tickets/work | Ticket system | Reference/index + analysis |
| Original documents | Source repository | Store/manage according to policy |
| Continuity metadata | EKCP | System of record |
| Handover state | EKCP | System of record |
| Audit ledger | Audit subsystem | System of record |
| Embeddings | Vector index | Rebuildable derived index |

## 7. Engineering target

The project should be enterprise-quality in boundaries, security, reliability, auditability, governance, testing, observability and recovery. It does not need unnecessary distributed infrastructure.
