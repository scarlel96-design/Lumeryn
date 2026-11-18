# Grok Build에 전달할 보조 작업지시서

**전달 시점**: Codex 1차 작업에서 계약·작업 경로·권한이 확정되고, 별도 Worktree가 준비된 후. Antigravity의 3B와 병행 가능하다.

---

프로젝트: Lumeryn
작업: WO-AGENT-00 / 3A — Grok Build 독립 시험
역할: Codex의 보조 리뷰·독립 구현 담당

시작 절차를 최우선으로 수행하라. `AGENTS.md`, `docs/MASTER_PLAN.md` 전체, `docs/PROJECT_STATE.md`, `docs/WORK_ORDERS/WO-AGENT-00.md`, `docs/DECISIONS/ADR-0001-foundation.md`를 모두 읽어라. 이전 대화·요약으로 대체하지 마라. `python scripts/verify_project.py check --wo WO-AGENT-00`를 실행하라. 마스터 SHA-256, 담당 범위와 작업 폴더를 첫 보고에 표시하라.

수행 작업:
1. Codex가 승인한 Worktree에서만 작업하라.
2. Grok Build 버전·실행 명령·출력 형식·프로젝트 지침 인식을 확인하라.
3. 승인된 읽기 전용 테스트를 수행하라.
4. 명령 종료 상태와 실제 결과물을 분리해 기록하라.
5. 지정된 테스트 파일만 변경할 수 있다. 그 외 파일은 변경하지 마라.
6. 결과에 실행 명령, 실제 로그, 변경 파일, 블로커, 미실시 시험을 포함하라.

금지:
- 메인 브랜치 쓰기, 외부 Push, 비밀정보 수집, 다른 AI의 Worktree 수정, 정책·아키텍처 변경, 무단 설치.
- 미확인 결과를 PASS로 보고하는 행동.

산출물: `docs/REPORTS/M0-grok-smoke.md` 또는 Codex가 지정한 독립 인계 경로.

Codex가 통합 승인하기 전에는 멈춰라.