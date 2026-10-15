# 001. Use Postgres + pgvector as the vector store

- **Status:** Proposed
- **Date:** 2026-10-15

## Context

Retrieval needs dense vector search over ~50k chunks with metadata filtering (tenant,
ticker, fiscal year, section) and a lexical index for hybrid search. Postgres is already
in the stack for tenants, documents and the audit of ingestion runs. No measurement yet;
the ablation table (README) will carry the numbers.

## Decision

We will store embeddings in Postgres 16 with pgvector (HNSW index) and use Postgres
full-text search for the BM25 leg of hybrid retrieval. One datastore, one backup, one
set of row-level security rules for tenancy.

## Alternatives

| Option | Why rejected |
|--------|--------------|
| Qdrant | Native hybrid search and better HNSW tuning, but a second datastore to operate, back up and tenant-scope. Revisit if pgvector recall or latency misses the SLO. |
| Weaviate | Same as Qdrant with a heavier footprint. |
| Pinecone | Managed and fast, but per-tenant isolation and cost are opaque, and a vendor dependency for a project whose point is "I did not add a datastore I did not need". |

## Consequences

**Positive:** one datastore; tenant filter and RLS apply to vectors and metadata alike;
hybrid search needs no second system.

**Negative, debt accepted:** HNSW build time and memory on a laptop; pgvector's filtered
search can degrade recall when filters are selective (pre-filter vs post-filter) and this
must be measured.

**Revisit when:** recall@10 on the golden set with filters drops more than 5 points
against unfiltered, or p95 retrieval exceeds the 150 ms budget at 50k chunks.
