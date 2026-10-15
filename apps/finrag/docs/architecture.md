# Architecture — finrag

C4 container level. Dashed boundary = authenticated, tenant-scoped zone. Arrows are
labelled with protocol and payload. Boxes marked *(later)* arrive in the milestone named.

## Containers

```mermaid
flowchart LR
    U[Analyst<br/>browser / API client] -->|HTTPS POST /query<br/>question, tenant| API[FastAPI<br/>app/main.py]

    subgraph tenant [Tenant-scoped zone — ADR 003]
        API -->|rewrite, decompose,<br/>extract filters| QU[Query understanding<br/>(retrieval milestone)]
        QU -->|BM25 via Postgres FTS| PG[(Postgres 16 + pgvector<br/>chunks, metadata, RLS)]
        QU -->|dense top-50| PG
        PG -->|RRF fusion| RR[Cross-encoder reranker<br/>bge-reranker-v2-m3 (later)]
        RR -->|top 5–8 chunks| GEN[Grounded generation<br/>structured claims + citations]
    end

    GEN -->|chat completion, streamed| LLM[LLM provider<br/>via P3 gateway later]
    GEN -->|SSE: claims, citations| U

    subgraph ingest [Ingestion pipeline — make setup]
        EDGAR[SEC EDGAR 10-K / 10-Q] -->|download| PARSE[Parser<br/>tiered: PyMuPDF → Docling → vision]
        PARSE -->|structure-aware chunks<br/>ADR 002| CHUNK[Chunker + metadata]
        CHUNK -->|embed, upsert by content hash| PG
    end

    API -.->|OTel traces, cost per stage| OBS[Langfuse / Phoenix<br/>(harden milestone)]
```

## Primary request flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant Q as Query understanding
    participant P as Postgres (pgvector + FTS)
    participant R as Reranker
    participant G as Generation
    participant L as LLM
    C->>A: POST /query {question, tenant_id, filters}
    A->>A: validate (Pydantic), bind request_id + tenant
    A->>Q: rewrite / decompose / extract filters
    Q->>P: BM25 top-50 AND dense top-50 (tenant filter in repository layer)
    P-->>Q: fused top-50 (RRF)
    Q->>R: rerank
    R-->>G: top 5–8 chunks
    G->>L: prompt with delimited, labelled context
    L-->>G: structured claims[] each with source_chunk_id
    G->>G: verify every citation exists in the retrieved set; else refuse
    G-->>C: 200 streamed {answered, claims, citations} + X-Request-ID
```

## Components

| Box | Lives at | Responsibility |
|-----|----------|----------------|
| API | `app/main.py` | HTTP, request id, validation, health |
| Query understanding | `app/query.py` *(later)* | rewrite, decomposition, metadata filters, HyDE (each toggleable) |
| Retrieval | `app/retrieval/` *(later)* | hybrid BM25 + dense, RRF, tenant filter (ADR 003) |
| Reranker | `app/rerank.py` *(later)* | cross-encoder over the shortlist |
| Generation | `app/generate.py` *(later)* | context assembly, structured output, citation verification, refusal |
| Ingestion | `ingest/` *(later)* | parse, chunk (ADR 002), embed, idempotent upsert |
| Golden set + eval | `data/golden_set.jsonl`, `evals/` | the real deliverable; gates merges |

## External systems

| System | Used for | Failure handling |
|--------|----------|------------------|
| SEC EDGAR | corpus download at setup | retry with backoff; partial corpus is logged, never silent |
| LLM provider | generation, LLM-as-judge | see `docs/failure-modes.md` F1–F3, F7 (harden milestone) |
| Postgres | everything stateful | F9/F10: `/health` → `db: down`, fail fast with 503 |

## Trust boundaries

- User input and **retrieved document text are both untrusted**. Document text is
  delimited and labelled as data in the prompt (indirect prompt injection is the defining
  RAG attack; P6 red-teams it).
- Model output is parsed against `QueryResponse`; a citation that does not resolve to a
  retrieved chunk is dropped and, if none remain, the answer becomes a refusal.
