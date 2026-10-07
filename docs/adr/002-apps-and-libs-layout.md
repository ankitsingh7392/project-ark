# 002. Lay the monorepo out as apps/ and libs/, and extract a library only after a pattern repeats

- **Status:** Accepted
- **Date:** 2026-10-07

## Context

The repository holds deployable AI services and, in time, code they share.
The directory names should tell a reader at a glance which is which. Two
services exist today (`ats`, `lexiscan`) and they share no code. The tempting
move is to build shared libraries up front (evaluation harness, observability
helpers, an LLM client wrapper) so that future services start from a platform.
The risk is building abstractions for needs that do not exist yet, which
produces a `common/` or `utils/` folder that becomes a dumping ground.

## Decision

We will use two top-level code directories:

| Directory | Holds | Exists today |
|-----------|-------|--------------|
| `apps/` | Deployable products and services. Each is a standalone uv project (ADR 001) held to `CHECKLIST.md`. | Yes |
| `libs/` | Reusable code consumed by two or more apps. Each library is its own uv project with its own tests. | No. Created with the first extracted library. |

A library is extracted from apps into `libs/` only when **the same pattern has
been implemented in at least two apps** and the duplication is causing real
cost. The progression is: app A → app B → repeated pattern observed → extract →
A and B migrate → app C consumes. We do not build libraries first and apps
around them.

Candidates we expect to earn extraction first, in order, once a second app
needs them: evaluation (dataset loading, metric runners, baseline comparison,
reporting), observability (logging, request-ID middleware, metrics, tracing
setup), security (input validation, auth, tool permission checks, audit
events). An LLM client or retrieval library is extracted only when two apps use
a provider or a retrieval stack, and then as thin primitives (retries,
timeouts, token accounting, structured output), never as a wrapper that hides
model-specific behaviour.

Names that will not be created: `common/`, `utils/`, `helpers/`, `core/`, or
any single library that claims to be the framework.

## Alternatives

| Option | Why rejected |
|--------|--------------|
| Keep `projects/` with shared code inside one of the apps | A reader cannot tell deployable services from shared code. Shared code hidden in one app makes that app a dependency of the others. |
| Create `libs/evaluation`, `libs/observability`, `libs/llm`, `libs/retrieval` now | No second consumer exists. The abstractions would be guesses, and every guess that turns out wrong is migration work. It also contradicts CONSTITUTION §4. |
| `packages/` instead of `libs/` | Equivalent. `apps/` and `libs/` is the more common pairing and reads unambiguously. |

## Consequences

**Positive:** the top level answers "what is deployable?" and "what is shared?"
by name. Libraries that exist are known to have two real consumers, so their
interfaces were shaped by use. The extraction rule is written down, so
reviewers can push back on premature abstraction by citing it.

**Negative, debt accepted:** for a while two apps will carry similar
boilerplate (logging setup, a request-ID middleware, an eval runner). That
duplication is the evidence that justifies the eventual extraction.

**Revisit when:** a third app appears, or two apps have duplicated a non-trivial
module and a bug had to be fixed in both.
