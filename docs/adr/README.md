# Architecture Decision Records

Repository-wide decisions. Each module keeps its own ADRs under
`projects/<module>/docs/adr/` for decisions that only affect that module.

Format: [`docs/templates/adr.md`](../templates/adr.md). Numbers are
zero-padded and never reused. A superseded ADR stays in place with its status
updated.

| ADR | Decision | Status |
|-----|----------|--------|
| [001](001-standalone-uv-project-per-module.md) | Each module is a standalone uv project with its own lockfile | Accepted |
| [002](002-apps-and-libs-layout.md) | Lay the monorepo out as `apps/` and `libs/`; extract a library only after a pattern repeats | Accepted |
