# Architecture — <module>

## Containers

Every process, datastore, external system and the user is a box. Model
components are their own boxes labelled with the artifact or provider. Dashed
boundaries mark authenticated zones.

```mermaid
flowchart LR
    U[Client] -->|POST /endpoint| A[API process]
    A --> P[Preprocess]
    P --> M[Model<br/>artifact or provider]
    M --> A
    A -->|JSON| U
    subgraph data [Data]
        D[(datastore)]
    end
    A --> D
```

## Primary request flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant M as Model
    C->>A: POST /endpoint
    A->>A: validate (Pydantic)
    A->>M: infer
    M-->>A: result
    A-->>C: 200 JSON
```

## Components

| Box | Lives at | Responsibility |
|-----|----------|----------------|
| API process | `app/main.py` | ... |
| Model | `data/<artifact>` or `<provider>` | ... |

## External systems

| System | Used for | Failure handling |
|--------|----------|------------------|
| ... | ... | see `docs/failure-modes.md` F-n |
