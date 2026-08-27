# Reproducible Demo

## Goal

Demonstrate the product through one coherent employee-departure scenario.

## Scenario

1. A critical employee is identified.
2. The system shows concentrated knowledge/ownership risk.
3. Authorized knowledge is retrieved.
4. Documentation/knowledge gaps are identified.
5. A handover is created.
6. Tasks and knowledge package are generated.
7. A successor is recommended with explanation.
8. A manager approves the sensitive step.
9. Ownership/access actions are executed through backend controls.
10. Verification completes.
11. Audit history shows the important events.

## Demo requirements

**Hard requirement (ADR-014):** the viva/demo path must not depend on live external API availability. Required external data and AI outputs must be prefetched, cached, or otherwise made deterministic before the demonstration. This is not a "where appropriate" preference — a rate-limit error or flaky third-party API during the viva is a demo failure, treated with the same severity as a functional bug.

```text
Development integration mode → live APIs allowed
Viva/demo mode                → live external dependencies prohibited
```

Use:
- seeded development/demo data,
- pre-fetched and cached connector outputs (GitHub/Jira/Confluence/Google Drive) captured ahead of time, not fetched live during the presentation,
- pre-computed or cached AI outputs for the scripted demo path, with the live path available only as a fallback demonstration of graceful degradation — not the primary path.

The demo should also include one visible failure/degradation path and show graceful recovery — this is the one place a live/simulated failure is intentional and controlled, not accidental.
