# Engineering Constitution

**Status:** Authoritative
**Scope:** Every project and shared component in this repository

---

## Purpose

This repository exists to demonstrate one capability:

> **Taking an AI technique from a real problem to a useful, measurable, reliable product.**

It does not optimise for the number of frameworks, models, agents or services
used. It optimises for **usefulness, evidence, engineering quality and sound
technical judgement**.

This document states the principles. The documents below turn them into
things that can be checked:

```text
CONSTITUTION.md          "AI behaviour must be measurable."
     │
     ▼
CHECKLIST.md             "Every project has an evaluation dataset."
     │                   "A quality threshold is defined."
     │                   "A regression fails CI."
     ▼
apps/<name>/         The implementation, plus its own CHECKLIST.md
     │                   recording evidence for each requirement.
     ▼
CI / evaluation gate     The check that runs on every pull request.
```

| Document | Answers |
|----------|---------|
| `CONSTITUTION.md` | How we build. The principles. |
| `CHECKLIST.md` | What must be true before a project is done, and how a reviewer verifies it. |
| `CONTRIBUTING.md` | How day-to-day work happens: branches, commits, pull requests. |
| `docs/standards/` | The detailed engineering standard behind each checklist section. |
| `docs/adr/` | Why specific repository-wide decisions were made. Each project keeps its own ADRs too. |
| `docs/templates/` | Files to copy when starting a project or a decision record. |

---

## 1. Build Products, Not Demos

Every substantial project starts with a clear problem. We should be able to say:

* who has the problem;
* what they are trying to accomplish;
* why it is worth solving;
* where AI provides real leverage;
* how we will know the solution is useful.

A project is not valuable because it uses an LLM, an agent, retrieval or any
other technique.

> **Technology is the means. User value is the outcome.**

## 2. Measure AI Behaviour

AI output is probabilistic. A few examples that look right do not show that a
system works.

Where AI behaviour matters we define measurable criteria and test against them:
correctness, groundedness, retrieval quality, tool-use accuracy,
structured-output validity, safety behaviour, latency, cost.

Changes to models, prompts, retrieval, tools or orchestration are evaluated for
regression before they merge.

> **If quality matters, measure it.**

## 3. Evidence Over Claims

We prefer demonstrated results to statements about quality.

| Do not say | Show |
|------------|------|
| "Fast." | p95 latency 1.4 s at 50 concurrent requests, 1,000-request run, 4 vCPU. |
| "Accurate." | Macro-F1 0.937 on the documented evaluation set, n = 240. |
| "Low cost." | £0.009 per request under the stated assumptions. |

Claims about performance, quality, reliability and cost are reproducible by
someone who did not build the system.

> **If we cannot demonstrate it, we are careful about claiming it.**

## 4. Simple Architecture First

We choose the simplest architecture that solves the actual problem. Complexity
must have a reason.

We do not add agents because they are fashionable, microservices because they
look serious, a vector database because every AI project "needs" one, a second
model without a measured benefit, or infrastructure the problem does not
justify.

> **Simple → measurable → scalable when necessary.**

Architecture evolves in response to real requirements, not imagined future ones.

The same rule governs shared code. A library is extracted into `libs/` when a
pattern has been proven across two or more apps, not because reuse feels
elegant. The progression is app A, then app B, then a repeated pattern, then
extraction. We do not build libraries first and apps around them, and we do not
create a `common/` or `utils/` folder (see [ADR 002](docs/adr/002-apps-and-libs-layout.md)).

## 5. Production-Minded Engineering

A project does not need to run at scale to show production-quality thinking.
It does need to consider reliability, security, observability, performance,
cost, failure behaviour, maintainability and operational load.

The question is not "can this work?" It is:

> **"What would happen if people actually depended on this?"**

## 6. Make Systems Observable

A system that cannot be diagnosed is hard to operate and hard to improve.

Systems provide structured logs, useful metrics, traces, request IDs, error
context, and visibility into model, tool and retrieval calls. We should be able
to answer: why was this request slow, which call consumed the time, did
retrieval fail, which tool failed, why did the evaluation regress, what did the
request cost.

Observability never exposes sensitive data as a side effect.

> **If something matters in production, we can see it.**

## 7. Design for Failure

Failures are normal. Models time out, providers rate-limit, APIs disappear,
retrieval returns nothing, models produce malformed output, networks drop.

Systems have intentional behaviour for every important failure mode: validated
inputs and outputs, bounded retries, timeouts, graceful degradation, fallbacks,
actionable errors, protection for downstream systems.

> **Failure behaviour is part of the product.**

## 8. Security by Default

Security is considered during design, not added at the end.

We protect credentials, secrets, user data, internal services, external
integrations, and the tools an AI system may call. External input is untrusted.
For AI systems we consider prompt injection, data leakage, excessive tool
permissions, unsafe tool execution, malicious retrieved content and insecure
handling of model output.

We favour least privilege and explicit permissions.

> **An AI system has only the capabilities it actually needs.**

## 9. Cost Is a Product Constraint

Quality is not the only optimisation target. We treat quality, latency,
reliability and cost as a single trade-off and understand the major cost
drivers of every project.

Where practical we measure or estimate cost per request, per 1,000 requests,
and at expected scale, and we name the single biggest lever for reducing it.

> **A solution that works but cannot economically operate is not finished.**

## 10. Automate What Should Not Depend on Memory

Human judgement is valuable. Human memory is not a quality-control system.

Linting, type checking, tests, security scanning, dependency checks, evaluation
regression and build verification run automatically. The goal is not maximum
automation. The goal is:

> **Make the correct path easy and stop known mistakes reaching users silently.**

## 11. Document Important Decisions

For significant decisions we record context, alternatives, the decision,
trade-offs and consequences, as Architecture Decision Records.

The roads not taken matter because they show judgement. A future engineer
should understand:

> **Why this solution exists, not just how it works.**

## 12. Keep Learning Visible

This repository is allowed to evolve. We expect to replace models, remove
technologies, simplify architectures, improve evaluations and learn from
failures. Changing our minds on better evidence is good engineering.

> **Strong engineers are not attached to their first implementation.**

## 13. Prefer Working Software Over Ceremony

Documentation, standards, ADRs and diagrams exist to support engineering. They
are not the product. We never spend more effort making a project look rigorous
than making it useful and technically sound.

> **Working, measurable software beats impressive paperwork.**

## 14. Exceptions Are Allowed

These principles guide good decisions. They are not a reason to add complexity.
A project may deviate when there is a clear reason, and the deviation is
recorded in an ADR when it materially affects architecture, security, quality,
cost or reliability.

We optimise for **appropriate engineering**, not compliance theatre.

---

## The Standard

For every substantial project we can answer, with evidence:

> What problem does this solve?
> Why does AI belong here?
> How do we know it works?
> How good is it?
> How fast is it?
> What does it cost?
> How does it fail?
> How do we observe it?
> How is it secured?
> Why was it designed this way?
> What would we change at the next scale?

Answering those with evidence shows more than the ability to use AI. It shows
the ability to **engineer AI products**.

> **Build for users. Measure what matters. Keep the architecture honest. Make failure visible. Know the cost. Prove the result.**
