# Task 030 — `apps/api/app/modules/risk/bus_factor_engine.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 011 (project repository), Task 024 (ingestion worker — needs real contribution/ownership signal to calculate from)
**Requirements:** REQ-A002 (calculate continuity risks: bus factor, undocumented knowledge, orphaned assets), ADR-009 (deterministic risk calculations, not opaque LLM scores)
**Board ref:** `tasks/BOARD.md` — Phase 9.1
**Owner:** Sanmati

## Goal

A deterministic, explainable bus-factor and Knowledge Continuity Score (KCS) calculation — per ADR-009, this must not be an LLM-generated number; it's a transparent formula over real ownership/activity data.

## Scope

- `apps/api/app/modules/risk/bus_factor_engine.py`
- Bus-factor calculation per project (how concentrated is ownership/knowledge among few individuals) using data available from `project_members`, asset ownership, and ingested activity signals (e.g. GitHub contribution data via the ingestion worker).
- KCS (Knowledge Continuity Score) as a composite, documented formula — not a black box; the exact inputs and weighting must be written down so the score is explainable to a viva panel, consistent with ADR-009.
- Writes results to `risk_assessments` (`docs/DATABASE.md` §2).

## Out of scope

- Documentation staleness/divergence signals — Task 031, which likely feeds into or alongside this engine's inputs.
- AI-generated narrative explanations of a risk score — the Risk Agent (Task 041) may summarize this task's deterministic output in natural language, but the underlying number itself must remain deterministic and LLM-free, per ADR-009.

## Implementation notes

- This is a core academic/defensible claim of the project (explainable deterministic risk scoring) — document the exact formula and its inputs clearly enough that it could be defended question-by-question in a viva, not just implemented correctly in code.

## Acceptance criteria

- [ ] Bus-factor and KCS are computed deterministically from real project/ownership/activity data — same input state always produces the same score.
- [ ] The formula and its inputs are documented clearly enough to explain in one paragraph, per-project.
- [ ] Results are written to `risk_assessments` with enough detail to reconstruct why a score came out the way it did.

## Tests

- [ ] Unit — formula correctness against hand-computed expected scores for known synthetic ownership distributions
- [ ] Integration — calculation against real ingested project data from Task 024
- [ ] Security — n/a
- [ ] E2E — n/a yet

## Documentation updates

`docs/REQUIREMENTS.md` or a new short risk-methodology note — document the exact KCS/bus-factor formula if not already specified precisely enough in existing docs.

## Known limitations

_Fill in at completion._
