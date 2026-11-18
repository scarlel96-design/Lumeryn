# Codex에 **가장 먼저** 입력할 작업지시서

다음 텍스트를 새 Codex 세션에 전달한다. 프로젝트 루트에서 실행한다. 사용자 PC의 실제 경로는 로컬에서 확인한다.

---

프로젝트: Lumeryn
작업: WO-AGENT-00 / 1차 — 총괄 사전 점검 및 작업 계약
역할: Codex Lead Engineer

**절대 선행 규칙**: 어떤 코드·설정·프로세스·모델도 수정하기 전에 `AGENTS.md`, `docs/MASTER_PLAN.md` 전체, `docs/PROJECT_STATE.md`, `docs/WORK_ORDERS/WO-AGENT-00.md`, `docs/DECISIONS/ADR-0001-foundation.md`를 이 순서로 읽어라. 과거 대화나 요약으로 대체하지 마라. `python scripts/verify_project.py check --wo WO-AGENT-00`를 실행하라. 첫 응답에 마스터 설계서 SHA-256과 관련 절 번호, 현재 WO 상태, 선행조건, 변경 허용 경로를 요약해라. 읽기나 검사가 실패하면 HOLD하고 변경을 중단하라.

목표:
1. 현재 PC의 Codex, Grok Build, Antigravity CLI 설치·버전·인증 가능 상태를 조사한다.
2. 현재 Git 저장소·브랜치·미커밋 변경·기준 커밋을 확인한다.
3. 기존 SearchAI-Starter 프로토타입이 있다면 별도 기록한다. 무단으로 덮어쓰지 않는다.
4. 세 AI의 역할, 독립 테스트, Git Worktree 경로, 변경 금지 경계를 확정한다.
5. `docs/REPORTS/`에 환경 조사, 작업 계약, 명령·권한 계획을 작성한다.
6. Grok/Antigravity에 보낼 개별 지시서를 확인하고 실제 배포 가능 조건을 점검한다.
7. 지침 또는 스크립트가 실제 환경과 맞지 않으면 원인과 안전한 수정안을 제시한다.

제한:
- 아직 제품 코드, 모델 학습, 검색 엔진, UI를 개발하지 마라.
- 무단 설치, 로그인 우회, 전역 설정 변경, 외부 Push, 배포, 비밀정보 출력, 무제한 권한 설정을 금지한다.
- 보조 AI를 아직 호출하지 마라. 먼저 공통 작업 계약과 Worktree/권한 조건을 확정하라.
- 테스트하지 않은 작업을 PASS로 기록하지 마라.

완료 보고:
- 마스터 SHA-256 및 열람 확인
- 실제 실행한 명령과 관측 결과
- 생성·수정한 파일
- 보조 AI 작업 시작 가능 여부
- HOLD/GO 판단과 필요한 사용자 승인

이 단계가 끝나면 다음 보조 AI 지시서 전달 전에 멈춰라.