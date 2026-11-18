# ADR-0001 — Lumeryn architecture and development governance

- Status: **ACCEPTED FOR DESIGN** (not implementation completion).
- Date: 2026-11-18
- Decision owner: product owner; integration: Codex.

## Decision

1. Use Qwen3.5-4B as the initial core model, with source verification and vision.
2. Keep search as a default core feature.
3. Add specialists via Tool, LoRA adapter, or independent specialist-model modules.
4. Use Clean Architecture, SoC, dependency inversion and a modular monolith.
5. Keep Windows 11 native window controls and Snap Layouts; follow Apple HIG for internal UI.
6. Codex leads. Grok Build and Antigravity CLI run only delegated, isolated work.
7. Every new WO or session must read the entire master plan, current state, and WO.
8. Record actual test evidence before marking tasks complete.

## Rejected alternatives

- Grow a single giant model for every specialty.
- Introduce microservices for all functionality before they are necessary.
- Start three AI workers for every task.
- Treat prompts as an enforcement boundary for tool permissions.

## Follow-up

Validate architecture with contract tests and recorded model/system benchmarks.
Change decisions with a new ADR and corresponding master-plan update.
