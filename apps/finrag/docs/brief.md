# FinRAG — one-page brief

> Roadmap P1 ① milestone 1. Written before any retrieval code. Edit freely; this is the
> opening paragraph of the README and the first 20 seconds of the interview story.

## The sentence

**FinRAG answers an equity analyst's questions about SEC 10-K / 10-Q filings with the
stated figure and a citation to the filing page, and refuses when the filing does not
contain the answer.**

## User and job

| | |
|---|---|
| **User** | A sell-side / buy-side equity analyst (secondary: a credit officer, a compliance reviewer) at a mid-size financial-services firm. |
| **Job** | Pull a specific figure, a table value, or a period-over-period change out of a 200-page filing, with the page it came from, fast enough to stay in flow. |
| **Today** | Ctrl-F in the PDF, or trusting a chatbot that cannot show its source. |
| **Why RAG, not search** | The number is often only in a table, phrased differently from the question, and the analyst needs the *derived* answer ("margin changed by 1.4 points") with both source rows cited. |

## Five real example questions (also rows g0001–g0005 of the golden set)

1. What was Apple's total net sales for fiscal year 2023? *(simple lookup)*
2. According to the segment table in Apple's FY2023 10-K, what were net sales for the Services segment? *(table extraction)*
3. How did Apple's gross margin percentage change between fiscal 2022 and fiscal 2023? *(multi-hop)*
4. Which of Apple and Microsoft reported higher total revenue for fiscal year 2023? *(comparative)*
5. What was Apple's total net sales for fiscal year 2030? *(unanswerable — must refuse)*

## What "correct" means

A correct answer is the figure as stated in the filing, with a citation that resolves to the
document and page containing it. A fabricated citation is a failure even if the figure is
right. For an unanswerable question, the only correct response is a refusal.

## Service-level objective

| Measure | Target | Measured by |
|---|---|---|
| Correctly cited answers on the answerable golden set | ≥ 85 % | `make eval` (citation validity × answer correctness) |
| Refusal rate on the unanswerable golden set | ≥ 90 % | `make eval` |
| Hallucinated citation rate | ≤ 2 % | `make eval` |
| p95 time to first token, streamed | < 3 s | `make bench`, C=20, laptop label |
| Concurrency | 20 users | `make bench` |
| Corpus | ≥ 500 filings, ~50k chunks | ingestion report |

## Explicitly out of scope

- Real-time market data, prices, or anything not inside a filing.
- Advice, forecasts, or opinions. The system reports what the filing says.
- Filings before 2019 or outside SEC EDGAR.
- A polished UI. A thin page that shows the answer, citations and the trace is enough.

## Corpus and benchmark

SEC EDGAR 10-K / 10-Q filings (free, real, messy, tables everywhere). Public comparison via
[FinanceBench](https://github.com/patronus-ai/financebench) once the pipeline exists.
