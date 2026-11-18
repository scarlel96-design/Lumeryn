# Lumeryn 장기 프로젝트 운영과 세션 복구 규약

> 목적: 수개월 이상 개발 중 설계·작업 범위·차단 이력과 검증 증거를 잃지 않는다.

## 1. 기준 문서

1. `AGENTS.md` — 공통 실행 지침
2. `docs/MASTER_PLAN.md` — 전체 제품/아키텍처 설계의 단일 기준
3. `docs/PROJECT_STATE.md` — 현재 진행 상황의 단일 현황표
4. `docs/WORK_ORDER_INDEX.md` — 계획 및 WO 의존성
5. `docs/WORK_ORDERS/<WO-ID>.md` — 개별 작업 계약
6. `docs/DECISIONS/ADR-*.md` — 중요한 설계 결정 이력

요약본이나 채팅 이력으로 마스터 전체 열람을 대체할 수 없다.

## 2. 매 WO 시작

```powershell
py -3.12 scripts/verify_project.py check --wo WO-AGENT-00
py -3.12 scripts/verify_project.py read --wo WO-AGENT-00
py -3.12 scripts/check_architecture.py
```

각 개발 AI는 실제로 위 문서를 읽고, 시작 보고에 `master_sha256`와 관련 장·필수 조건·수정 범위를 남긴다.
검사 스크립트만 실행했다고 문서를 이해한 것으로 간주하지 않는다.

## 3. 작업 상태 및 수락

- `NOT_STARTED`: 아직 시작하지 않음.
- `READY`: 작업 명세 승인, 선행조건 확보.
- `IN_PROGRESS`: 실행 및 테스트 진행.
- `BLOCKED`: 인증·권한·환경 등의 외부 장애.
- `HOLD`: 테스트 미실시, 검증/승인 부족.
- `FAILED`: 완료 조건을 충족하지 못함.
- `COMPLETED`: 수락 기준과 실제 증거 확인.

프로세스 종료 코드 0은 성공 판정의 필요조건이 될 수 있지만 충분조건이 아니다.

## 4. 최소 인계 증거

`schemas/agent-handoff.schema.json`을 따른다.
- 담당 AI, WO, 적용 마스터 SHA
- 기준 커밋과 작업 브랜치·Worktree
- 실제 명령과 종료 코드
- 생성된 파일·테스트 결과·미해결 사항
- 모델/CLI 버전과 가능한 사용량 측정값

```powershell
py -3.12 scripts/validate_contracts.py handoff path/to/handoff.json
```

이 검사는 **형식 및 마스터 해시**를 확인한다. Git 커밋과 로그·시험의 실제 존재 및 진실성은 Codex가 별도로 검증한다.

## 5. 작업 종료

1. 실제 테스트 결과를 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED`로 보고한다.
2. `docs/PROJECT_STATE.md`에 작업 상태·커밋·검증 증거를 남긴다.
3. 설계가 바뀌면 ADR와 마스터 설계서를 함께 변경한다.
4. 테스트 실패·미실시 항목을 삭제하지 않는다.
5. 통합은 Codex의 검수 및 필요 시 사용자 승인 후 진행한다.

## 6. GitHub 운영 권고

- `main`은 통합 기준선으로 보존한다.
- 변경은 `agent/<name>-<wo>`, `feature/<name>`, `hardening/<name>` 등 독립 브랜치에서 수행한다.
- PR에는 설계 영향, 실제 테스트, 미실시 시험, 다음 WO를 기록한다.
- 프로젝트에서 GitHub Branch Protection/Rulesets를 사용해 PR/필수 CI를 강제하도록 검토한다.
- 관리자 권한이 있어도 보호 규칙을 무효화하는 강제 Push를 자동화하지 않는다.

현재 GitHub 설정에 보호 규칙이 실제 적용되었는지는 별도로 확인해야 한다.

## 7. 사용량 최소화

- 단순 작업은 Codex만 사용한다.
- 독립 작업이 명확할 때만 Grok Build와 Antigravity CLI를 병행한다.
- 전체 마스터 설계서를 읽은 뒤에는 관련 파일/로그만 상세 검토한다.
- 공급자마다 사용량 단위가 달라 혼합 합산하지 않는다.
- 실패한 명령은 원인 분석 없이 반복 실행하지 않는다.
- GPU 집중 작업은 하나만 실행하도록 잠금한다.

## 8. 작업 중단·재개

새 세션에서 가장 먼저 `PROJECT_STATE.md`와 현재 브랜치, 실제 Git 상태를 대조한다.
커밋되지 않은 변경은 삭제하거나 강제로 덮어쓰지 않는다.
이전에 완료했다고 기록된 WO도 근거가 없으면 완료를 재확인해야 한다.
