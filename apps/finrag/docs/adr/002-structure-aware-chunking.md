# 002. Chunk by document structure, never split a table

- **Status:** Proposed
- **Date:** 2026-10-15

## Context

SEC filings have a fixed section hierarchy (Item 1A, Item 7, Item 8) and the figures the
user asks for live inside tables. A fixed character window cuts tables in half and loses
the row/column relationship, which is where naive RAG reads the wrong year's number.

## Decision

We will chunk on section boundaries with a target of 500–800 tokens and 10–15 % overlap,
keep every table whole (as Markdown) inside a single chunk, and prefix each chunk with a
breadcrumb header ("Apple Inc · FY2023 10-K · Item 7 MD&A · Segment Results"). Chunking is
a pure, unit-tested function; "a table is never split" is an assertion in the test suite.

## Alternatives

| Option | Why rejected |
|--------|--------------|
| Fixed-size recursive splitter (1000/200 defaults) | Baseline only. Splits tables; this is the single most common reason RAG underperforms on filings. Kept as ablation row 1. |
| Semantic chunking (embedding-similarity breakpoints) | Expensive at ingest, non-deterministic, and does not understand tables. |
| Whole-section chunks | Too long for the context budget and poor embedding quality. |

## Consequences

**Positive:** table-extraction questions become answerable; citations map to a section
and page; metadata (section, page range) comes for free.

**Negative, debt accepted:** depends on a parser that detects tables reliably (the parsing
milestone); very large tables may exceed the chunk budget and need small-to-big retrieval.

**Revisit when:** the ablation table shows structure-aware chunking buys fewer than 3
points of recall over the baseline.
