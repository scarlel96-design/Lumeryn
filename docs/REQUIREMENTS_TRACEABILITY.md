# Lumeryn — requirements-to-work tracking

This is the initial traceability map. The master plan contains detailed P0/P1/P2 requirements.

| Requirement | Work Orders | Validation | Status |
|---|---|---|---|
| Qwen3.5-4B core + image input | WO-02/04/10 | Real model/vision E2E | NOT_RUN |
| Search core always available | WO-07~16 | Search independent of optional plugins | NOT_RUN |
| Retrieval planning/evidence | WO-08/12~15 | Source/claim trace tests | NOT_RUN |
| Optional Tool/LoRA/Specialist module | WO-MOD-01/02 | Toggle/unload/permissions | NOT_RUN |
| Search model remains 4B-based | WO-05/FT-02~04 | Registry and VRAM tests | NOT_RUN |
| User-owned policy, ethics/refusal rules | WO-06/17 | Version/rollback/decision tests | NOT_RUN |
| Clean Architecture + SoC | WO-03 and all | Contract/import boundary tests | NOT_RUN |
| Native Win11 frame/Snap | WO-UI-01 | Actual Windows display tests | NOT_RUN |
| Apple HIG design and spring motion | WO-UI-02/03 | UI/DPI/accessibility tests | NOT_RUN |
| Codex main, Grok/Antigravity optional | WO-AGENT-00/01 | Actual CLI/Worktree smoke | NOT_RUN |
| Whole master plan read every WO | AGENTS + verify script | Hash report + human/agent start report | DOCUMENT_RULE |
| BF16 LoRA/search/vision fine-tuning | FT-01~04 | Holdout benchmark/regression | NOT_RUN |
| Model/update rollback | REL-01~03 | Recovery tests | NOT_RUN |

Add new requirements together with the associated WO and acceptance evidence. Never mark a requirement complete solely from document existence.

## Foundation quality requirements (v1.1)

| Requirement | Evidence location | Status |
|---|---|---|
| GOV-01: master chapters ordered and WO file exists | `scripts/verify_project.py`, CI | CI_VALIDATION_REQUIRED |
| GOV-02: reports must refer to current master hash | `scripts/validate_contracts.py`, schema | CI_VALIDATION_REQUIRED |
| ARCH-01: domain/application import boundary | `scripts/check_architecture.py` | CI_VALIDATION_REQUIRED |
| MOD-05: module metadata contract | `schemas/module-manifest.schema.json`, example | METADATA_ONLY |
| SEC-01..12: trust boundaries and sandbox policy | `docs/SECURITY_MODEL.md` | DESIGN_ONLY |
| DATA-01: candidate/approved/eval separation | `docs/DATA_GOVERNANCE.md` | DESIGN_ONLY |
| GOV-03: Windows+Linux offline CI | `.github/workflows/ci.yml` | CI_VALIDATION_REQUIRED |
| GOV-04: continuation and draft next WO | `docs/OPERATIONS_AND_STATE.md`, WO-AGENT-01 | DRAFT |

## 추가 검증 경계

| 요구 | 관련 산출물 | 현재 상태 |
|---|---|---|
| MODEL-05: model manifest | `schemas/model-manifest.schema.json` | METADATA_ONLY |
| POL-04: policy rule schema | `schemas/policy-rule.schema.json` | METADATA_ONLY |
| UI-09: Win11 + Apple HIG 실측 | `docs/UI_SPEC.md` | NOT_RUN |
| PERF-01: 리소스·검색 호출 예산 | `docs/PERFORMANCE_BUDGET.md` | DESIGN_ONLY |
| GOV-05: 문서 상대 링크·순환 import | CI, `scripts/check_docs_links.py` | CI_VALIDATION_REQUIRED |
