# Codex에 마지막으로 전달할 통합 작업지시서

**전달 시점**: Grok과 Antigravity의 독립 결과가 모두 도착한 후. 실패·미실시는 명시한다.

---

프로젝트: Lumeryn
작업: WO-AGENT-00 / 최종 — 검증·통합·판정
역할: Codex Lead Engineer

작업 시작 규칙에 따라 `AGENTS.md`, `docs/MASTER_PLAN.md` 전체, `docs/PROJECT_STATE.md`, `docs/WORK_ORDERS/WO-AGENT-00.md`, 관련 ADR를 다시 읽고 `python scripts/verify_project.py check --wo WO-AGENT-00`를 실행하라. 시작 보고에 마스터 SHA-256과 관련 설계 절을 적어라.

1. Grok과 Antigravity의 보고서를 읽고 실제 로그와 변경 파일을 대조하라.
2. 도구 성공 응답과 실제 산출물·테스트 성공을 구분하라.
3. 승인된 범위의 Git 변경만 검토하라.
4. 스키마 검사·Worktree 격리·권한 설정의 테스트 결과를 기록하라.
5. 미실시 테스트를 PASS로 처리하지 마라.
6. `docs/REPORTS/M0-final-report.md`를 작성하라.
7. `docs/PROJECT_STATE.md`에 현재 상태·블로커·다음 단계·검증 로그를 갱신하라.
8. GO/HOLD/NO-GO를 실제 기준으로 판정하라.
9. 주요 설계 변경이 필요하면 ADR을 작성하고 사용자에게 영향과 이유를 보고하라.
10. 승인 없는 외부 Push·배포는 금지한다.

최종 보고에 실행 명령, 테스트, 변경 파일, 마스터 SHA-256, 최종 상태를 포함하라. 완료하더라도 다음 WO를 자동 시작하지 마라.