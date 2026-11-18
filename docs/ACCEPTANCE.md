# Lumeryn — acceptance and release gate

## Verification evidence

- `PASS`: executed check with reproducible evidence.
- `FAIL`: executed check did not meet acceptance.
- `SKIP`: explicitly skipped with reason.
- `NOT_RUN`: not executed; never claim a pass.
- `BLOCKED`: cannot execute due to a prerequisite.
- `HOLD`: cannot authorize next step.

## Gate WO-AGENT-00

1. Confirm repository state, CLI installation and authentication **on user's actual machine**.
2. Verify each CLI's read-only smoke output and permissions.
3. Establish distinct worktrees for Grok and Antigravity.
4. Record structured handoff with real command statuses.
5. Verify no tool modifies the integration branch during delegated work.
6. Update `docs/PROJECT_STATE.md` with evidence and next WO.

An offline documentation test is not a substitute for these checks.

## General release gate

- Required contract, unit, integration, visual and end-to-end tests pass.
- Domain does not import infrastructure/Qt/vendor SDK.
- Optional modules can be disabled without breaking default search.
- Claim-to-source citations and image inputs are tested.
- No unauthorized file/network/tool execution.
- Windows native close/minimize/maximize, Snap, keyboard, DPI and Reduce Motion work.
- Model+vision processor+tokenizer compatibility is verified for exported LoRA.
- Actual RAM/VRAM/latency and search accuracy are measured.
- No critical open security or data-integrity regressions.
- Release has verified rollback plan.

## Benchmarks

Baseline model, baseline-plus-retrieval and trained-model-plus-retrieval must run on the same test set. The 500-question dataset and target thresholds are proposals until measured.
