# 003. Enforce the tenant boundary in the repository layer, backed by row-level security

- **Status:** Proposed
- **Date:** 2026-10-15

## Context

Documents belong to tenants. The failure that matters is not "a filter is slow" but "a
filter is forgotten" and tenant B sees tenant A's documents, through retrieval, the
reranker, or a cache.

## Decision

We will apply the tenant filter in the data-access layer from the authenticated request
context. It is never a parameter the caller passes and never optional. Postgres row-level
security is enabled on every tenant-scoped table as a second, independent layer. Every
cache key includes `tenant_id`. An integration test seeds two tenants, queries as A, and
asserts zero B chunks in retrieval, rerank and cache paths; it runs in CI.

## Alternatives

| Option | Why rejected |
|--------|--------------|
| Filter at the call site (`WHERE tenant_id = :t` in each query) | A developer can forget it. It will eventually be forgotten. |
| Schema or collection per tenant | Strong isolation but operationally heavy for 10 simulated tenants, and migrations multiply. Reasonable at hundreds of tenants; not now. |
| Separate database per tenant | Same, heavier. |

## Consequences

**Positive:** isolation is structural, testable and documented; per-tenant usage
accounting falls out of the same context.

**Negative, debt accepted:** RLS adds planner overhead; connection pooling must set the
tenant for each session; a shared HNSW index across tenants means filtered recall must be
measured (see ADR 001).

**Revisit when:** a single tenant exceeds ~1M chunks or a customer requires physical
isolation.
