# Lumeryn — Work Order road map

Read `docs/MASTER_PLAN.md` and `docs/PROJECT_STATE.md` before any WO. A listed WO is **not** complete until actual tests and evidence exist.

| Order | WO | Lead | Parallel support | Dependency | Deliverable |
|---:|---|---|---|---|---|
| 1 | WO-AGENT-00 | Codex | Grok+Antigravity (conditional) | Blueprint | CLI/worktree/permissions verification |
| 2 | WO-AGENT-01 | Codex | Grok implement, Antigravity review | AGENT-00 | Dispatcher/usage tracker (DRAFT until AGENT-00 GO) |
| 3 | WO-01 | Codex | Antigravity | M0 | Hardware report |
| 4 | WO-02 | Codex | Antigravity | WO-01 | Original Qwen evaluation |
| 5 | WO-03 | Codex | Grok | WO-02 | Clean skeleton and CI hardening |
| 6 | WO-04 | Codex | Grok test | WO-03 | LLMProvider + vision |
| 7 | WO-05 | Codex | Grok review | WO-04 | Model Registry |
| 8 | WO-MOD-01 | Codex | Grok/Antigravity | WO-03 | Module SDK contracts |
| 9 | WO-06 | Codex | Grok tests | WO-03 | Policy gateway |
| 10 | WO-07 | Codex | Grok implement | WO-03/06 | SearchProvider |
| 11 | WO-08 | Codex | Antigravity review | WO-04/07 | Search planning |
| 12 | WO-09 | Grok delegated | Antigravity compatibility | WO-07 | HTML/PDF fetch |
| 13 | WO-10 | Codex | Antigravity | WO-04/09 | Image retrieval |
| 14 | WO-11 | Grok delegated | Codex integrate | WO-03/09 | Evidence store |
| 15 | WO-12 | Codex | Grok | WO-11 | Qdrant hybrid index |
| 16 | WO-13 | Codex | Antigravity | WO-12 | Embedding/Reranker |
| 17 | WO-14 | Codex | Grok | WO-11/13 | Claim verification |
| 18 | WO-15 | Codex | Grok | WO-08/14 | LangGraph research orchestration |
| 19 | WO-16 | Codex | Antigravity | WO-10/15 | Multimodal E2E |
| 20 | WO-17 | Codex | Grok | WO-06 | Policy Studio |
| 21 | WO-18 | Codex | Grok | WO-05 | Model Studio |
| 22 | WO-MOD-02 | Codex | Grok/Antigravity | MOD-01/06 | Module manager/routing/isolation |
| 23 | WO-UI-01 | Codex | Antigravity | WO-03 | Win11 native frame/Snap |
| 24 | WO-UI-02 | Codex | Grok | UI-01 | HIG design tokens/QML |
| 25 | WO-UI-03 | Codex | Grok | UI-02 | Motion/accessibility |
| 26 | WO-19 | Codex | Grok | Core/UI/Policy | Desktop integration |
| 27 | WO-20 | Codex | Grok+Antigravity | M2 | Evaluation datasets |
| 28 | WO-21 | Codex | Grok+Antigravity | WO-19/20 | Security/stability |
| 29 | WO-22 | Codex | Read-only reviews | WO-21 | Release gate |
| 30 | FT-01 | Codex | Grok/Antigravity | WO-02/08 | Curated training dataset |
| 31 | FT-02 | Codex | Antigravity | FT-01/WO-20 | Search LoRA |
| 32 | FT-03 | Codex | Antigravity | FT-02/WO-20 | Evidence reasoning LoRA |
| 33 | FT-04 | Codex | Antigravity | WO-16/FT-01 | Vision LoRA |
| 34 | FT-05 | Codex | Grok review | FT-03/04 | Optional DPO |
| 35 | FT-06 | Codex | Antigravity | FT-03/20 | Optional GRPO |
| 36 | REL-01 | Codex | Antigravity | Stable FT | Model export |
| 37 | REL-02 | Codex | Grok | WO-22/REL-01 | Installer |
| 38 | REL-03 | Codex | Read-only reviews | REL-02 | Updater/rollback |

The master plan and each detailed WO own final scope. The roadmap alone does not authorize code changes.

## Long-term gates (v1.1)

- `WO-AGENT-01` has a **DRAFT** specification. It cannot start until WO-AGENT-00 is GO.
- Every WO must run the design-document check and include a start report with `master_sha256`.
- Core/import architecture guard and JSON handoff/module validation are part of the initial CI.
- Search/model/GUI/CLI hardware tests must remain NOT_RUN until executed.
- Technical risk controls: [Security](SECURITY_MODEL.md), [Data](DATA_GOVERNANCE.md), [Modules](MODULE_CONTRACTS.md).
