# Task 047 — `apps/api/tests/test_gemini_rate_limiter.py`

**Status:** backlog
**Priority:** P0
**Depends on:** Task 045 (test harness), the already-implemented `gemini_rate_limiter.py`/`gemini_client.py`
**Requirements:** AGENTS.md's non-negotiable Gemini rate-limiting rule; the project's known hard ceiling of 15 RPM / 250,000 TPM / ~1,000 RPD with a 4.0–4.5s inter-call delay
**Board ref:** `tasks/BOARD.md` — Phase 15.3
**Owner:** Paras

## Goal

Prove the rate limiter actually holds under realistic concurrent load — not just unit-level correctness, since this specific rule was once accidentally dropped from `AGENTS.md` during a documentation rewrite and had to be restored; a load test is the guardrail that catches a future *code* regression the same way the doc fix caught the *documentation* regression.

## Scope

- `apps/api/tests/test_gemini_rate_limiter.py`
- A test that fires concurrent requests through `gemini_client.py` (from multiple simulated callers, e.g. several agents from Phase 13 all calling at once) and confirms the rolling 60-second RPM/TPM window and the 4.0–4.5s inter-call delay are actually enforced under real concurrency, not just when called sequentially from a single thread.
- A test confirming the daily (~1,000 RPD) soft cap behavior and the typed `GeminiLimitError` is raised correctly when exceeded, rather than the call silently proceeding or crashing unpredictably.

## Out of scope

- Modifying `gemini_rate_limiter.py`/`gemini_client.py` themselves unless the test reveals an actual bug — this task's job is to prove correctness, not to redesign working code.

## Implementation notes

- This is explicitly the regression-prevention task for the rate-limit rule that was once dropped — treat a failing or flaky result here as a release blocker, not a nice-to-have, precisely because this rule has already proven itself easy to silently lose once.

## Acceptance criteria

- [ ] Concurrent calls from multiple simulated callers never exceed the RPM/TPM ceiling.
- [ ] The 4.0–4.5s inter-call delay is observably enforced under concurrent load, not just sequential calls.
- [ ] Exceeding limits raises the typed `GeminiLimitError`, never a raw/unhandled exception or a silent pass-through.

## Tests

- [ ] Unit — n/a — this file is itself the test
- [ ] Integration — n/a — covered above
- [ ] Security — n/a
- [ ] E2E — this test should be runnable in CI (Task 048) on every change touching the LLM Gateway, as a standing regression guard

## Documentation updates

None expected — this operationalizes an existing `AGENTS.md`/ways-of-working rule rather than changing it.

## Known limitations

_Fill in at completion._
