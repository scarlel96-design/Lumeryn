# Lumeryn 프로젝트 상태 기록 — 장기 작업 이어가기의 단일 현황표

> 상태 문서 ID: SA-STATE-001  
> 기준일: 2026-11-18  
> **상태는 설계 초기값이다. 이 문서를 작성했다고 실제 구현을 완료한 것은 아니다.**

## 1. 현재 기준선

| 항목 | 값 |
|---|---|
| 현재 마일스톤 | M0 — 3중 개발 에이전트 환경 |
| 현재 WO | WO-AGENT-00 |
| 현재 상태 | READY — 아직 실제 사용자 PC에서 실행하지 않음 |
| 주담당 | Codex |
| 보조 담당 | Grok Build / Antigravity CLI |
| 첫 실행 선행조건 | 실제 저장소 위치, CLI 설치/인증, 사용자 PC 환경 확인 |
| 통합 브랜치 | `main` (GitHub 저장소 초기화 확인) |
| 현재 마스터 설계서 | `docs/MASTER_PLAN.md` v1.1.0 |
| 다음 WO | WO-AGENT-01 (현재 미작성·미승인) |
| 1차 릴리스 상태 | NOT_STARTED |

## 2. 작업 상태 원칙

`NOT_STARTED` / `READY` / `IN_PROGRESS` / `BLOCKED` / `HOLD` / `FAILED` / `COMPLETED`.

- `READY`: 계획 및 WO가 존재하지만 실행 전.
- `COMPLETED`: 수락 기준·실제 검증 로그·승인 근거가 있을 때만 가능.
- `HOLD`: 승인 또는 중요한 선행조건 필요.
- `BLOCKED`: 환경·권한·외부 종속성에 의해 진행 불가.
- 다른 WO로 이동해도 현재 문제·리스크를 삭제하지 않는다.

## 3. 마일스톤 표

| 마일스톤 | 상태 | 시작 | 완료 | 설명 |
|---|---|---|---|---|
| M0 | READY | - | - | 개발 AI 운영기반 |
| M1 | NOT_STARTED | - | - | 모델·코어 기반 |
| M2 | NOT_STARTED | - | - | 기본 검색 코어 |
| M3 | NOT_STARTED | - | - | 추론·모듈·정책·UI |
| M4 | NOT_STARTED | - | - | 안정판·평가 |
| M5 | NOT_STARTED | - | - | 본격 파인튜닝 |
| M6 | NOT_STARTED | - | - | 정식 배포 |

## 4. Work Order 상태

| WO | 상태 | 담당 | 결과/근거 |
|---|---|---|---|
| WO-AGENT-00 | READY | Codex(Lead), Grok, Antigravity | 실행 전; 지시서만 작성됨 |
| WO-AGENT-01 | DRAFT / NOT_STARTED | Codex(Lead), Grok/Antigravity 조건부 | 작업 문서 작성됨. WO-AGENT-00 GO 전 착수 불가 |
| WO-01~WO-22 | NOT_STARTED | 마스터 계획 참조 | 각 WO 생성 전 |
| WO-MOD-01~ | NOT_STARTED | 마스터 계획 참조 | 각 WO 생성 전 |
| WO-UI-01~ | NOT_STARTED | 마스터 계획 참조 | 각 WO 생성 전 |
| FT-01~FT-06 | NOT_STARTED | 마스터 계획 참조 | 기준 평가 전 |
| REL-01~REL-03 | NOT_STARTED | 마스터 계획 참조 | 출시 전 |

## 5. 아직 확인하지 못한 정보

- 사용자 PC의 Windows 11 빌드, CPU/GPU와 VRAM/RAM
- Codex/Grok/Antigravity의 현재 설치 버전·인증·모델·사용량
- 현재 Git 저장소의 실제 경로·브랜치·원격 설정
- 기존 SearchAI-Starter의 소스 통합 여부
- 모델 추론/비전/학습의 실제 속도·호환성

## 6. 최근 검증 이력

| 시각 | 작업 | 결과 | 기록 위치 |
|---|---|---|---|
| 2026-11-18 | 마스터 설계서·작업 규칙·첫 WO 문서 생성 | 문서 작성(실제 CLI 테스트 아님) | 현 파일, docs/WORK_ORDERS/WO-AGENT-00.md |

## 7. 블로커·위험 로그

| ID | 위험 | 상태 | 조치 |
|---|---|---|---|
| RISK-001 | 보조 CLI의 실제 설치·권한 동작 미확인 | OPEN | M0에서 검증 |
| RISK-002 | 3중 병렬 실행이 실제 사용량을 늘릴 수 있음 | OPEN | 시간·쿼터 측정 후 결정 |
| RISK-003 | 기본 모델 학습 자원 미확인 | OPEN | WO-01에서 VRAM 조사 |

## 8. 다음 세션 재개 지침

1. `AGENTS.md`와 `docs/MASTER_PLAN.md` **전체**를 다시 읽는다.
2. 이 파일의 현재 단계·WO·블로커를 확인한다.
3. 해당 WO를 읽고 `scripts/verify_project.py check --wo ...`를 실행한다.
4. `COMPLETED`라고 기록된 항목이라도 보고서와 실제 변경 증거가 없는 경우 확인을 요구한다.
5. **첫 작업: `WO-AGENT-00`**. 아직 실제 CLI 환경 검증은 수행하지 않았다.
6. 작업 완료 시 이 파일을 같은 커밋에 업데이트한다.

## 9. 결정 및 변경 로그

| 날짜 | 변경 | 승인/근거 | 영향 |
|---|---|---|---|
| 2026-11-18 | Clean Architecture + Modular Core + UI 디자인 + 3중 AI 운영 설계 동결 | 사용자 요구사항 | 마스터 v1.0.0 |
## 10. 원격 저장소 초기화

- 저장소: `https://github.com/scarlel96-design/Lumeryn`
- 기본 브랜치: `main`
- 초기 GitHub 상태: README만 존재. 설계서와 스캐폴드를 최초로 추가하는 단계.
- 이 기록은 실제 세 CLI의 실행 성공을 뜻하지 않는다.


## 11. GitHub 초기 커밋 및 검증 (2026-11-18)

- GitHub 저장소: https://github.com/scarlel96-design/Lumeryn
- 설계·초기 골격 반영 커밋: `d48400a54338acf485cc4a918c9b0c3405cce0de`
- 반영 범위: 마스터 설계, AGENTS, 첫 WO, AI별 지시서, Python 계약 골격, 문서 검사·테스트·GitHub Actions.
- GitHub Actions Foundation checks: **PASS** — https://github.com/scarlel96-design/Lumeryn/actions/runs/44221424259
- 첫 작업 이슈: https://github.com/scarlel96-design/Lumeryn/issues/1
- **중요:** CI PASS는 문서 검사·계약 단위 테스트에 한정된다. 실제 Codex/Grok/Antigravity CLI 연결과 Qwen 추론은 **NOT_RUN**.
- 다음 조치: 사용자 PC에서 WO-AGENT-00을 실행하고 실제 실행 결과를 기록한다.

## 12. 개발 기반 정밀 점검 및 보강 (2026-11-18)

- 작업 브랜치: `hardening/foundation-audit-20261118`
- 변경 PR: https://github.com/scarlel96-design/Lumeryn/pull/2
- 검토 범위: 자동 문서검사, Clean Architecture import 검사, 인계/모듈 JSON 계약, Windows/Linux CI, 보안/데이터 거버넌스, 후속 WO 초안.
- 해당 변경은 **개발 준비 보강**이며, WO-AGENT-00의 실제 CLI 동작 검증 완료를 의미하지 않는다.
- `docs/MASTER_PLAN.md`의 24장에 보강 설계를 기록했다.
- 스키마 검사·정적 검사는 실제 플러그인 샌드박스 또는 AI 추론 안전성을 증명하지 못한다.
- 프로그램의 실제 검색, 이미지 분석, 학습, UI는 여전히 **NOT_RUN / NOT_IMPLEMENTED**.
- GitHub CI 검증 및 병합 결과는 변경 커밋의 Checks를 기준으로 별도 확인한다.
- 다음 실제 실행: WO-AGENT-00 (M0) 시작. 완료 전 WO-AGENT-01 수행 금지.

## 13. 보강 검토 보고서

- 리뷰: [FOUNDATION_REVIEW_2026-11-18.md](FOUNDATION_REVIEW_2026-11-18.md)
- PR #2는 커밋 `5b259ea468e291b44c071eaa343345a915a53c64`로 `main`에 병합되었다. [Main CI](https://github.com/scarlel96-design/Lumeryn/actions/runs/44224806143)가 PASS임을 확인했다.
- WO-AGENT-00은 실제 PC에서 아직 실행하지 않았다.

## 14. 보강 PR 병합 확정 (2026-11-18)

- PR: https://github.com/scarlel96-design/Lumeryn/pull/2 — **MERGED**.
- 최종 기본 브랜치 커밋: `5b259ea468e291b44c071eaa343345a915a53c64`.
- PR CI: https://github.com/scarlel96-design/Lumeryn/actions/runs/44224672008 — **PASS (Windows/Ubuntu)**.
- Main CI: https://github.com/scarlel96-design/Lumeryn/actions/runs/44224806143 — **PASS (Windows/Ubuntu)**.
- 이 PASS는 개발 문서·모델/모듈/정책 메타데이터·정적 아키텍처 검사·오프라인 단위 테스트에만 해당한다.
- 사용자 PC의 세 AI CLI, GPU, Qwen 추론, 비전, Win11 UI 실기 검증은 **NOT_RUN**.
- **M0 / WO-AGENT-00: READY 유지.** 다음 실제 작업은 사용자 PC 기반의 CLI·권한·Worktree 검증이다.
