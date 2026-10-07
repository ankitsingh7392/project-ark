# <module> — Definition of Done

- **Project type:** ML-SVC | LLM-SVC | RAG | AGENT
- **Standard:** [`/CHECKLIST.md`](../../CHECKLIST.md) at commit `<sha>`
- **Last full verification:** YYYY-MM-DD, commit `<sha>`

Status: `[x]` verified, `[ ]` not done, `[N/A]` with the rule that excludes it.
Every `[x]` has evidence: the command and its output line, or the artifact path.

## 1. Cold start
- [ ] 1.1 Prerequisites — evidence:
- [ ] 1.2 Env vars documented — evidence:
- [ ] 1.3 `.env.example` — evidence:
- [ ] 1.4 Reproducible install — evidence:
- [ ] 1.5 One-command start — evidence:
- [ ] 1.6 Dependencies auto-start — evidence:
- [ ] 1.7 Migrations — evidence:
- [ ] 1.8 Health check — evidence:
- [ ] 1.9 Cold-start CI job — evidence:

## 2. README
- [ ] All required headings present, none empty — evidence:

## 3. Architecture
- [ ] 3.1 Diagram source — evidence:
- [ ] 3.2 Container-level view — evidence:
- [ ] 3.3 Request data flow — evidence:
- [ ] 3.4 Model components explicit — evidence:
- [ ] 3.5 Retrieval / tool boundaries — evidence:
- [ ] 3.6 Trust boundaries — evidence:
- [ ] 3.7 README mirrors it — evidence:

## 4. ADRs
- [ ] 4.1 ≥ 3 ADRs — evidence:
- [ ] 4.2 Template followed — evidence:
- [ ] 4.3 Rejected options named — evidence:
- [ ] 4.4 Linked from README — evidence:

## 5. Tests + CI
- [ ] 5.1 Unit tests — evidence:
- [ ] 5.2 Integration tests — evidence:
- [ ] 5.3 Smoke test — evidence:
- [ ] 5.4 Lint — evidence:
- [ ] 5.5 Type check — evidence:
- [ ] 5.6 Coverage floor — evidence:
- [ ] 5.7 CI matrix entry — evidence:
- [ ] 5.8 Branch protection — evidence:

## 6. Evaluation
- [ ] 6.1 Dataset committed — evidence:
- [ ] 6.2 Metric defined — evidence:
- [ ] 6.3 Runner — evidence:
- [ ] 6.4 Baseline recorded — evidence:
- [ ] 6.5 Regression threshold — evidence:
- [ ] 6.6 Runs in CI — evidence:
- [ ] 6.7 Reproducible — evidence:
- [ ] 6.8 Prompt/model changes trigger eval — evidence:

## 7. Observability
- [ ] 7.1 Structured logs — evidence:
- [ ] 7.2 Request ID — evidence:
- [ ] 7.3 Per-request timing — evidence:
- [ ] 7.4 Stage timing — evidence:
- [ ] 7.5 Metrics endpoint — evidence:
- [ ] 7.6 Tracing — evidence:
- [ ] 7.7 Model calls observable — evidence:
- [ ] 7.8 Retrieval observable — evidence:
- [ ] 7.9 Errors with context — evidence:
- [ ] 7.10 No sensitive data in logs — evidence:
- [ ] 7.11 README evidence — evidence:

## 8. Four Numbers
- [ ] 8.1 Quality from §6 — evidence:
- [ ] 8.2 Benchmark runner — evidence:
- [ ] 8.3 Methodology in result — evidence:
- [ ] 8.4 Cost from §11 — evidence:
- [ ] 8.5 Minimum load — evidence:
- [ ] 8.6 README table generated — evidence:

## 9. Security
- [ ] 9.1 No secrets in history — evidence:
- [ ] 9.2 `.env` ignored — evidence:
- [ ] 9.3 Placeholders only — evidence:
- [ ] 9.4 Push protection on — evidence:
- [ ] 9.5 Dependency scan — evidence:
- [ ] 9.6 Dependencies constrained — evidence:
- [ ] 9.7 Input validation — evidence:
- [ ] 9.8 Request size limit — evidence:
- [ ] 9.9 Rate limiting — evidence:
- [ ] 9.10 Authentication — evidence:
- [ ] 9.11 Authorization — evidence:
- [ ] 9.12 Sensitive data not logged — evidence:
- [ ] 9.13 Model output validated — evidence:
- [ ] 9.14 Tool permissions — evidence:
- [ ] 9.15 Prompt injection — evidence:
- [ ] 9.16 Container scan — evidence:
- [ ] 9.17 Non-root container — evidence:

## 10. Failure behaviour
- [ ] 10.1 Failure table — evidence:
- [ ] 10.2 Each row has a test — evidence:
- [ ] 10.3 Timeouts tested — evidence:
- [ ] 10.4 Retries bounded — evidence:
- [ ] 10.5 No generic 500 — evidence:
- [ ] 10.6 Catch-all handler — evidence:
- [ ] 10.7 README mirrors it — evidence:

## 11. Cost
- [ ] 11.1 Unit economics — evidence:
- [ ] 11.2 Drivers itemised — evidence:
- [ ] 11.3 Assumptions explicit — evidence:
- [ ] 11.4 Biggest lever — evidence:
- [ ] 11.5 Token accounting — evidence:
- [ ] 11.6 Linked to measurement — evidence:

## 12. Demo
- [ ] 12.1 ≤ 3-minute demo — evidence:
- [ ] 12.2 Above the fold — evidence:
- [ ] 12.3 Real system — evidence:
- [ ] 12.4 Covers architecture, results, failure — evidence:
- [ ] 12.5 Reproducible — evidence:

## Final gate
- [ ] Every section above is `[x]` or a justified `[N/A]`
