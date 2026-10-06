# Task 056 — `apps/api/app/rag/evaluation_set.py`

**Status:** backlog
**Priority:** P1
**Depends on:** Task 027/028 (hybrid retrieval + permission filter — the thing being evaluated)
**Requirements:** REQ-A005 (evaluate retrieval/groundedness quality)
**Board ref:** `tasks/BOARD.md` — Phase 17.4
**Owner:** Mangirish

## Goal

A retrieval/groundedness evaluation set and runner — the evidence that the RAG pipeline's answers are actually grounded in retrieved sources, important both for genuine quality assurance and as viva-defensible proof of the system working as claimed.

## Scope

- `apps/api/app/rag/evaluation_set.py`
- A small, curated set of representative questions with known-good expected source documents/chunks (built from real ingested content, e.g. the GitHub-sourced demo data).
- A runner that executes each question through the real pipeline (Task 027/028, and the LLM synthesis step feeding Task 029) and reports retrieval precision/recall against the known-good sources, plus a basic groundedness check (does the answer actually cite the retrieved sources, not fabricate claims beyond them).

## Out of scope

- Large-scale automated benchmark tooling — a focused, curated evaluation set matching the actual demo content is more valuable here than broad generic benchmarking.

## Implementation notes

- This directly supports the viva narrative — being able to show 'here's our evaluation set and here's how retrieval performs against it' is more defensible than an unverified claim that RAG 'works.'

## Acceptance criteria

- [ ] A curated evaluation set exists with known-good expected sources for each question.
- [ ] The runner reports retrieval precision/recall and a groundedness signal against real pipeline output.
- [ ] Results are reproducible given the same underlying ingested data.

## Tests

- [ ] Unit — scoring logic against known synthetic retrieval results
- [ ] Integration — a full run against the real pipeline and real demo data
- [ ] Security — n/a
- [ ] E2E — n/a — this task is itself an evaluation harness

## Documentation updates

`docs/AI.md` — reference this evaluation set as the project's retrieval/groundedness quality check.

## Known limitations

_Fill in at completion._
