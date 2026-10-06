# Task 031 — `apps/api/app/modules/risk/doc_divergence_detector.py`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 024 (ingestion worker), Task 030 (bus-factor engine — shares the `risk_assessments` model/pattern)
**Requirements:** REQ-A002 (documentation staleness/gaps as a continuity risk)
**Board ref:** `tasks/BOARD.md` — Phase 9.2
**Owner:** Sanmati

## Goal

Detect signals that documentation has gone stale relative to the code/project it describes — a deterministic heuristic, consistent with ADR-009's 'no opaque LLM scoring' principle.

## Scope

- `apps/api/app/modules/risk/doc_divergence_detector.py`
- A heuristic comparing documentation update recency/content against code/project activity (e.g. a README untouched for N months while the underlying code changed heavily) using data already available from the GitHub connector/ingestion worker.
- Writes findings into `risk_assessments` alongside Task 030's output, or a clearly related structure — coordinate the exact shape with Task 030 so Phase 11's Documentation Agent (Task 040) has one consistent place to read from.

## Out of scope

- LLM-based semantic comparison of doc content vs. code behavior — that's squarely the Documentation Agent's job (Task 040), which may call an LLM; this task's detector must remain deterministic per ADR-009.

## Implementation notes

- Keep the heuristic simple and explainable first — a correct, simple staleness signal (e.g. time-since-last-doc-update vs. code-activity-ratio) is more defensible in a viva than a sophisticated but opaque one.

## Acceptance criteria

- [ ] Detector produces a deterministic staleness signal from real ingested project data.
- [ ] Output integrates cleanly with Task 030's `risk_assessments` usage, confirmed by reading Task 030's actual implementation before finalizing this one.

## Tests

- [ ] Unit — heuristic correctness against synthetic known-stale and known-fresh cases
- [ ] Integration — detection against real ingested GitHub data
- [ ] Security — n/a
- [ ] E2E — n/a yet

## Documentation updates

None expected beyond what Task 030 documents.

## Known limitations

_Fill in at completion._
