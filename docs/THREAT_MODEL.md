# Threat Model

| Threat | Impact | Primary mitigation |
|---|---|---|
| Cross-organization data access | Critical | organization scoping + RLS + authorization tests |
| RAG ACL leakage | Critical | permission-aware retrieval + ACL synchronization |
| Prompt injection in documents | High | treat retrieved content as untrusted |
| Agent tool abuse | Critical | tool boundary + policy gate + approval |
| Compromised connector credential | High | secret management + least privilege + rotation |
| Webhook spoofing | High | signature validation + replay protection |
| Duplicate side effect | High | idempotency keys + uniqueness |
| Audit tampering | High | controlled writes + hash chain + verification/checkpoint |
| Stale/deleted source content | High | reconciliation + deletion propagation |
| Malicious upload | High | validation + scanning where feasible |
| LLM hallucination | Medium/High | RAG grounding + citations + evaluation |
| Unauthorized successor decision | Critical | recommendation-only + human approval |
