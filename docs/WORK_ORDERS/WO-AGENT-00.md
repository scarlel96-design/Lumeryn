# WO-AGENT-00 — Codex·Grok Build·Antigravity CLI 협업 기반 검증

> WO ID: `WO-AGENT-00`  
> 마일스톤: `M0`  
> 우선순위: `P0`  
> 현재 상태: `READY / NOT_EXECUTED`  
> 책임: `Codex (Lead)`  
> 보조: `Grok Build`, `Antigravity CLI`  
> 문서 작성일: `2026-11-18`  
> 정책: **매 에이전트가 매 작업 시작 시 `docs/MASTER_PLAN.md` 전체를 다시 읽는다.**

## 0. 중요 지침: 시작 전 무조건 읽기

**모든 작업과 세션 재시작에 적용된다. 단순 리뷰도 예외가 아니다.**

1. 프로젝트 루트의 `AGENTS.md`를 읽는다.
2. `docs/MASTER_PLAN.md`를 **처음부터 끝까지 전부** 읽는다.
3. `docs/PROJECT_STATE.md`를 읽는다.
4. 이 WO 파일을 읽는다.
5. `docs/DECISIONS/ADR-0001-foundation.md`를 읽는다.
6. `python scripts/verify_project.py check --wo WO-AGENT-00`를 실행한다.
7. **시작 보고에 마스터 SHA-256, 관련 설계 절, 수행 범위, 선행조건을 기록한다.**
8. 파일 누락·설계 충돌·선행조건 미충족 시 `HOLD`로 보고하고 코드 작업을 시작하지 않는다.

요약문·이전 대화·모델 기억은 전체 마스터 설계서 열람을 대체하지 않는다. `AGENTS.md`가 자동으로 읽혔다 해도 별도로 마스터 설계서를 읽는다.

## 1. 목적

세 CLI의 실제 설치·인증·권한·프로젝트 지침·비대화형 출력·결과 기록·작업 격리를 검증한다. 이후 Lumeryn 개발에서 세 AI를 안전하게 병행할 수 있는 운영 기반을 만든다.

**이 WO는 Lumeryn 제품 기능 구현이 아니다.** Qwen3.5-4B 학습, 웹 검색 코어, Qt UI 구현은 다음 WO에서 수행한다.

## 2. 선행조건 및 작업 시작 기준

- 본 설계 파일들이 실제 Git 저장소 또는 작업 디렉터리에 존재해야 한다.
- 세 CLI는 실제 설치 여부부터 조사한다. **사전 설치를 가정하지 않는다.**
- 로그인, 설치, 네트워크 사용, 유료 호출, 전역 환경 변경에 필요한 사용자 승인을 구분한다.
- Git 저장소가 아니면 `git init` 여부를 사용자/리드의 승인 규칙에 따라 결정한다.
- 최초 기준 커밋이 없다면 Worktree 생성은 **BLOCKED**로 표시하고 선행조건을 정리한다.
- 사용자의 다른 프로젝트나 로컬 비밀정보를 열람·수정하지 않는다.

## 3. 역할·범위·실행 시점

| 순서 | 담당 | 시작 조건 | 작업 내용 | 실행 방식 |
|---:|---|---|---|---|
| 1 | Codex | 전체 설계 문서 읽기 완료 | 현재 환경·Repo·CLI 상태 조사 및 계약 생성 | **먼저 단독** |
| 2 | Codex | 단계 1 완료 | 결과 스키마·보고서 위치·작업 경로·허용 범위 확정 | **먼저 단독** |
| 3A | Grok Build | 전용 Worktree·계약·승인 준비 | 정해진 범위에서 독립 CLI/지침 로딩/읽기 전용 검증 | **3B와 병행 가능** |
| 3B | Antigravity CLI | 전용 Worktree·계약·승인 준비 | 정해진 범위에서 독립 CLI/지침 로딩/기술 문서 검증 | **3A와 병행 가능** |
| 4 | Codex | 3A/3B 결과 도착 | 실제 파일·출력·권한·종료 코드 검증 | **순차** |
| 5 | Codex | 4 완료 | 비교 보고·진행 상태 갱신·GO/HOLD/NO-GO | **단독** |

같은 파일에 병행 쓰기를 금지한다. 이 WO의 첫 실행에서는 Grok/Antigravity 모두 **읽기 전용 검증을 우선**한다. 쓰기 테스트는 별도 Worktree와 승인된 임시 경로에서만 수행한다.

## 4. 사용자에게 직접 필요한 실행 준비

실제 PC에서 Codex가 아래 읽기 전용 명령을 우선 실행한다. 미설치 명령은 `NOT_INSTALLED`로 기록한다.

```powershell
# 프로젝트 경로 예시: 실제 폴더로 변경한다.
Set-Location C:\Lumeryn

# 설계 문서와 작업 전 상태 확인
Get-Content -Raw -Encoding UTF8 .\AGENTS.md
Get-Content -Raw -Encoding UTF8 .\docs\MASTER_PLAN.md
Get-Content -Raw -Encoding UTF8 .\docs\PROJECT_STATE.md
Get-Content -Raw -Encoding UTF8 .\docs\WORK_ORDERS\WO-AGENT-00.md

py -3.12 .\scripts\verify_project.py check --wo WO-AGENT-00

git status --short
git branch --show-current
git worktree list

codex --version
grok --version
agy --version
```

`py -3.12`가 없고 다른 Python이 이미 있는 경우, 먼저 설치된 버전을 조회한다. 환경을 확인하지 않은 상태에서 Python 설치 또는 PATH 변경을 강행하지 않는다.

**주의**: `Get-Content -Raw`는 문서 전체를 출력한다. 출력이 잘렸다면 실제 파일을 다시 분할해 끝까지 확인하고, 읽은 내용을 요약해야 한다. 출력만 생성했다고 모델이 충분히 이해했다고 주장하지 않는다.

## 5. Codex — 단계 1: 기존 상태 파악 및 작업 계약

### 5.1 책임

1. 로컬 설치·인증 상태를 조사한다. 비밀값은 출력하지 않는다.
2. 기존 Lumeryn 폴더/저장소와 `SearchAI-Starter-0.1.0` 존재 여부를 확인한다.
3. `AGENTS.md`와 마스터 설계서의 경계·충돌 여부를 검토한다.
4. 공통 작업 결과 스키마와 Read-Only Smoke Test를 설계한다.
5. Grok과 Antigravity에 할당할 읽기 범위·Worktree 경로를 결정한다.
6. 승인 없이 설치·외부 Push·무제한 권한 변경을 수행하지 않는다.
7. 시험 기준과 미확인 조건을 문서로 남긴다.

### 5.2 산출물

- `docs/REPORTS/M0-environment-inventory.md`
- `docs/REPORTS/M0-agent-contract.md`
- `docs/REPORTS/M0-command-and-permission-plan.md`
- `docs/REPORTS/M0-worktree-plan.md`
- 실제 시험 가능한 상태라면 `docs/REPORTS/M0-codex-smoke.md`

### 5.3 첫 단계 완료 기준

- 설치 여부, 인증 대기 여부, 버전 정보, Git 기준 커밋, Worktree 가능 여부가 정확히 기록됨.
- 최소 권한으로 실행할 도구 명령과 출력 평가 기준 확정.
- 서로 겹치지 않는 두 보조 AI의 작업이 명시됨.
- 실제 근거가 없는 성공 주장이 없음.

## 6. Grok Build — 단계 3A: 격리된 프로젝트 지침 및 CLI 검증

### 6.1 시작 조건

- Codex가 공통 스키마와 변경 금지 범위를 확정함.
- 실제 Worktree 경로와 작업 브랜치가 지정됨(읽기 전용만 하는 경우 별도 스냅샷 가능).
- `AGENTS.md`, `MASTER_PLAN.md` 전체, `PROJECT_STATE.md`, 이 WO를 읽음.
- `verify_project.py check` 통과 또는 사유 있는 `BLOCKED` 보고.

### 6.2 수행 작업

1. `grok --version`·`grok --help`로 CLI 지원 여부를 확인한다.
2. 저장소 지침(`AGENTS.md`)이 적용되는지 실제 작업 시작 보고에서 확인한다.
3. 주어진 범위의 Read-Only 코드/문서 점검을 수행한다.
4. 출력 모드(`plain`/`json`)와 종료 상태를 기록한다. 실제로 실행하지 못하면 `NOT_RUN`으로 남긴다.
5. 요구사항을 임의로 바꾸지 않는다. 메인 브랜치에 쓰지 않는다.
6. 테스트용 쓰기가 허용된 경우 전용 Worktree의 지정 경로만 수정한다.
7. 발생한 오류와 전제 조건을 재현 가능한 절차로 보고한다.

### 6.3 산출물

- `docs/REPORTS/M0-grok-smoke.md` (소유 Worktree에 기록하거나 Codex에게 결과 전달)
- 실행 명령·도구 버전·종료코드·지침 확인 증거·미해결 이슈.

## 7. Antigravity CLI — 단계 3B: 격리된 기술·명령 호환성 검증

### 7.1 시작 조건

Grok과 동일하되, 독립 Worktree/보고서를 사용한다.

### 7.2 수행 작업

1. `agy --version`·`agy --help`로 실제 설치 및 명령 옵션을 확인한다.
2. 저장소의 `AGENTS.md`와 전체 설계서 열람 규칙 적용을 확인한다.
3. 로컬 환경에서 Antigravity CLI의 비대화형 명령과 결과 형식을 검토한다.
4. 가능하면 별도의 읽기 전용 기술 조사 1건을 수행한다.
5. CLI 종료코드와 실제 도구 수행 여부를 **별도로 기록**한다.
6. 출력에 `soft-deny` 등 승인 제한이 있으면 성공 처리하지 않는다.
7. 사용량·토큰 값이 표시되지 않으면 `unknown`으로 보고한다.
8. 코어·메인 브랜치·Grok의 전용 파일을 수정하지 않는다.

### 7.3 산출물

- `docs/REPORTS/M0-antigravity-smoke.md`
- 실행 명령·모델/CLI 버전·권한 상태·검증 가능한 출력·미해결 이슈.

## 8. 결과 인계 스키마

예시 파일: `schemas/agent-handoff.schema.json`. 다음 필드를 요구한다.

```json
{
  "wo_id": "WO-AGENT-00",
  "agent": "grok",
  "status": "BLOCKED",
  "master_sha256": "sha256-from-current-file",
  "worktree": null,
  "base_commit": null,
  "result_commit": null,
  "commands_executed": [],
  "files_changed": [],
  "tests": [],
  "blockers": ["example: CLI not authenticated"],
  "usage": {"input_tokens": null, "output_tokens": null},
  "ready_for_review": false
}
```

위는 **형식 예시**이며 실행 결과가 아니다. `commands_executed`는 명령·종료코드·로그 경로를 포함한다. 완료 판정은 보고서 내용과 실제 검증 결과를 대조한 뒤 Codex가 내린다.

## 9. Worktree 운영

Worktree는 **Git 저장소에 첫 기준 커밋이 존재할 때** 생성한다. 사용자 작업 폴더에 이미 변경이 있다면 덮어쓰지 않는다.

```powershell
# 예시. 선행 조건이 만족되고 경로 중복이 없을 때만 실행.
Set-Location C:\Lumeryn
git status --short
git rev-parse --verify HEAD

git worktree add -b agent/grok-wo-agent-00 ..\Lumeryn-grok-WO-AGENT-00 HEAD
git worktree add -b agent/agy-wo-agent-00  ..\Lumeryn-agy-WO-AGENT-00 HEAD

git worktree list
```

브랜치가 이미 있거나 폴더에 기존 데이터가 있는 경우 작업을 중단한다. `--force` 옵션을 자동으로 사용하지 않는다.

## 10. 종료 상태·재시도·비용

- 프로세스가 Exit 0을 반환해도 필수 산출물이 없으면 `COMPLETED` 아님.
- 승인 차단·권한 실패·인증 오류는 `BLOCKED`로 분류한다.
- 환경 관련 일시 오류만 제한된 재시도를 고려한다. 중복 쓰기 작업은 자동 재시도하지 않는다.
- 보조 AI 작업은 각각 1회 시도로 시작한다. 추가 호출은 Codex가 테스트 결과를 보고 승인한다.
- 세 공급자의 토큰·쿼터는 서로 다른 단위이므로 혼합 합산하지 않는다.
- 실제 절감 효과를 말하려면 Codex 단독 베이스라인과 동일 품질의 비교 작업이 필요하다.

## 11. 수락 기준(AC) 및 GO/HOLD/NO-GO

| AC | 기준 | 확인 방법 |
|---|---|---|
| AC-01 | 모든 에이전트가 시작 시 전체 마스터 설계서를 다시 읽는 규정 존재 | AGENTS/WO 검사 및 시작 보고 |
| AC-02 | 현재 설치·인증·버전 상태 정확히 파악 | 실제 로컬 명령과 결과 |
| AC-03 | Codex/Grok/Antigravity 역할·병행 시점 명확 | 작업 분배 보고 |
| AC-04 | 실제 코드 경로·Worktree 격리 절차 검증 | Git Worktree 목록·변경 범위 |
| AC-05 | 보조 작업의 범위·출력 계약 검증 | 결과 JSON 스키마 검사 |
| AC-06 | 정상 종료·실제 성공·테스트가 분리됨 | 정상/실패/출력 누락 시나리오 |
| AC-07 | 비밀정보 노출·무제한 권한 허용 없음 | 로그·설정 점검 |
| AC-08 | 사용량/시간 결과 기록 방식 확보 | 계측 로그 또는 unknown 처리 |
| AC-09 | 작업 상태 및 다음 WO 기록 | `PROJECT_STATE.md` 검증 |
| AC-10 | 미실행 시험은 미실행으로 표기 | 보고서 검사 |

- **GO**: 위 필수 기능이 실제로 검증되고 블로커 없음.
- **HOLD**: 인증·설치·커밋·권한 등의 선행조건이 아직 준비되지 않음.
- **NO-GO**: 요구 권한 격리 실패, 오염된 결과, 중요한 보안 위반 또는 실제 테스트 실패.

## 12. 작업 종료 보고 양식

```text
WO: WO-AGENT-00
Status: GO | HOLD | NO-GO
Master SHA-256: <verified-hash>
Repo base commit: <sha or unknown>
Codex: PASS/FAIL/SKIP/NOT_RUN + evidence
Grok: PASS/FAIL/SKIP/NOT_RUN + evidence
Antigravity: PASS/FAIL/SKIP/NOT_RUN + evidence
Worktree isolation: PASS/FAIL/SKIP/NOT_RUN
Permissions: PASS/FAIL/SKIP/NOT_RUN
Handoff schema: PASS/FAIL/SKIP/NOT_RUN
Tests: name / actual command / result / log path
Unresolved risks: ...
Next WO: WO-AGENT-01 only after authorization
```

**이 WO가 완료되어도 `WO-AGENT-01`을 자동 실행하지 않는다.** 먼저 테스트 근거와 수정된 `PROJECT_STATE.md`를 확인한다.