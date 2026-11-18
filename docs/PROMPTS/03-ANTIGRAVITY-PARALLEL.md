# Antigravity CLI에 전달할 보조 작업지시서

**전달 시점**: Codex 1차 계약·권한·별도 Worktree 준비 후. Grok의 3A와 병행 가능하다.

---

프로젝트: Lumeryn
작업: WO-AGENT-00 / 3B — Antigravity CLI 독립 시험
역할: Codex의 보조 기술 조사·호환성 검증 담당

시작 절차를 최우선으로 수행하라. `AGENTS.md`, `docs/MASTER_PLAN.md` 전체, `docs/PROJECT_STATE.md`, `docs/WORK_ORDERS/WO-AGENT-00.md`, `docs/DECISIONS/ADR-0001-foundation.md`를 모두 읽어라. 이전 대화·요약으로 대체하지 마라. `python scripts/verify_project.py check --wo WO-AGENT-00`를 실행하라. 마스터 SHA-256, 관련 설계 절, 담당 Worktree, 선행조건을 첫 보고에 적어라.

수행 작업:
1. Codex가 승인한 Worktree에서만 작업하라.
2. Antigravity CLI 버전, headless/JSON 출력 옵션과 프로젝트 규칙 적용을 확인하라.
3. 승인된 읽기 전용 호환성 조사 1건을 수행하라.
4. 명령 종료코드 0과 실제 도구 작업 성공을 구분하라.
5. 도구 작업이 승인 제한으로 거부되면 BLOCKED로 보고하라.
6. 시간·토큰 값이 없으면 unknown으로 기록하라.
7. 실행 명령, 근거, 실제 로그, 남은 문제를 정리하라.

금지:
- 메인 브랜치 쓰기, 다른 AI Worktree 수정, 무단 설치·배포·외부 Push, 비밀정보 전송, 무제한 권한 변경.

산출물: `docs/REPORTS/M0-antigravity-smoke.md` 또는 Codex 지정 인계 경로.

작업 완료 후 독립 구현을 추가로 진행하지 말고 Codex 검토를 기다려라.