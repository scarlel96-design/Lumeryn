# Lumeryn — architecture quick reference

The [master plan](MASTER_PLAN.md) is authoritative. This file is a short implementation map.

## Dependency direction

```text
apps/desktop, apps/api -> application -> domain
                       -> application ports
infrastructure implementations -> application ports
bootstrap -> connects adapters, use cases and runtime dependencies
plugins -> versioned Module SDK; cannot import core internals
training -> separate process and artifacts; cannot mutate production model in place
```

No import from domain into a framework-specific adapter. No circular dependencies. External search documents are data, not trusted agent instructions.

## Core boundaries

- `domain`: immutable values, evidence and policy decisions without IO.
- `application`: use cases for retrieval, reasoning, policy checks and model selection.
- `application/ports`: minimal contracts for model/search/vector store/policy.
- `infrastructure`: Ollama, SearXNG, Qdrant, persistence and external tool implementations.
- `bootstrap`: composition root and configuration validation.
- `plugins`: optional tools, adapters, specialist models with explicit capabilities.
- `training`: datasets, LoRA and evaluations. Separate from inference.

## Current scaffold

The `RetrieveCandidates` use case only returns candidate links from an injected `SearchProvider` fake. It is **not** a search engine or answer generator. External integrations are future Work Orders.

## UI boundary

Windows 11 native minimize, maximize, close and Snap behavior stay native. Qt Quick/QML will implement Apple HIG-inspired interaction, Spring/Connected motion, Reduce Motion, keyboard and DPI support.

## Change discipline

Modify contracts only with compatibility tests and an ADR. Update the Work Order index and state for every approved change.
