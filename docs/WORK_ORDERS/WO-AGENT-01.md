# WO-AGENT-01 — 경량 AI Dispatcher 설계·구현 (DRAFT)

> **상태: DRAFT / NOT AUTHORIZED / NOT_STARTED.**
> 선행 조건: WO-AGENT-00 실제 CLI·권한·Worktree 검증 **GO**. 코드는 아직 구현하지 않았다.

## 0. 매 시작 시 필독

1. `AGENTS.md`를 읽는다.
2. `docs/MASTER_PLAN.md` **전체를 읽는다.**
3. `docs/PROJECT_STATE.md`와 `docs/WORK_ORDER_INDEX.md`를 읽는다.
4. 이 WO와 ADR-0001/0002, `docs/SECURITY_MODEL.md`를 읽는다.
5. `python scripts/verify_project.py check --wo WO-AGENT-01`를 실행한다.
6. `master_sha256`, 선행조건, 변경 범위와 시작 판단을 기록한다.
7. WO-AGENT-00에 GO 증거가 없다면 **HOLD**로 종료한다.

## 목표

Codex를 총괄로 유지하면서, 보조 두 CLI를 필요할 때만 실행하는 **결정적 Python Dispatcher**를 구현한다.

## 구현 범위 (승인 후)

- WO 계약 읽기 및 스키마 검증
- Codex/Grok/Antigravity CLI 어댑터와 읽기 전용 smoke 모드
- 공급자별 프로세스 타임아웃·자식 프로세스 종료
- Git Worktree 검사 및 파일 변경 범위 확인
- 실제 실행 로그/종료 코드/출력 포맷 검증
- 인계 JSON 구조 검사
- 공급자별 사용량·시간 기록(모르면 null)
- GPU 작업 잠금 및 재시도 제한
- 테스트 통과 후 Codex에 검토 대기 상태 전달

## 배분 (제안)

1. **Codex 먼저:** 계약, 프로세스 명세, OS 권한·실패 정책을 확정한다.
2. **Grok 병행:** 독립 JSONL/JSON 출력 파서의 순수 함수와 단위 테스트를 구현한다.
3. **Antigravity 병행:** Windows 프로세스 종료·CLI 비대화형 호환성을 조사한다.
4. **Codex 마지막:** 인계 결과 검증, 통합, Windows·Linux CI, 실패 시나리오.

## 금지

- 자동 Push, 자동 PR 병합, 무제한 권한 승인
- 자동 외부 CLI 로그인·결제
- 모델 로드나 웹 검색 제품 기능 구현
- 전체 저장소의 무차별 AI 프롬프트 전송
- 결과 없이 무한 재시도

## 완료 기준(제안)

- 설치되지 않은 CLI·인증 실패·타임아웃이 정확히 BLOCKED 처리
- 종료 코드 0이어도 산출물이 없으면 완료 판정 거부
- 정상/오류 JSON·JSONL 입력 파싱 테스트
- 잘못된 Worktree/수정 범위에 대한 차단
- 비용·사용량 수치의 null 처리 및 공급자별 구분
- 최소한의 실제 CLI 호출 증거와 재현 가능한 로그
- 전체 마스터 설계·상태 문서·WO 종료 보고 업데이트

본 문서의 존재는 구현 착수를 허가하지 않는다. Codex가 선행 GO 및 사용자 승인 범위를 확인한다.
