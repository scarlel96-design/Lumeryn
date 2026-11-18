# Lumeryn first-session runbook

## Prerequisites

1. Clone `https://github.com/scarlel96-design/Lumeryn`.
2. Open the repository root in a terminal.
3. Check Python 3.12 and Git; do not install packages without reviewing prerequisites.
4. Verify CLI installations and authentication separately; never assume tools are connected.

## Mandatory document gate

```powershell
py -3.12 scripts/verify_project.py check --wo WO-AGENT-00
py -3.12 scripts/verify_project.py read --wo WO-AGENT-00
```

The second command prints full documents. The agent must actually read them; a hash alone is not proof of reading.

## Offline checks

```powershell
py -3.12 -m unittest discover -s tests -p "test_*.py" -v
py -3.12 -m compileall -q src scripts tests
```

## Delegation sequence

1. Send `docs/PROMPTS/01-CODEX-START.md` to Codex.
2. Read Codex's initial contract, branch ownership and permissions review.
3. Only after preparation, run `02-GROK-PARALLEL.md` and `03-ANTIGRAVITY-PARALLEL.md` in isolated worktrees.
4. Collect reports and send `04-CODEX-INTEGRATE.md` to Codex.
5. Run independent checks. Do not automatically mark WO completed.
6. Update `docs/PROJECT_STATE.md`, evidence log and the next WO.

## Limits

No model weights, trained LoRA, search adapter, browser service or desktop GUI is included in this initial scaffold. Do not claim these were tested.

## Branch strategy

Keep `main` as the integration branch. Codex creates short-lived `agent/<provider>-<wo>` branches for independent tasks. Workers must not commit directly to `main`.
