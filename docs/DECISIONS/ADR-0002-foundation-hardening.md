# ADR-0002 — 개발 기반 품질 게이트·모듈 계약 보강

- 날짜: 2026-11-18
- 상태: **DESIGN ACCEPTED, 코드 검증은 CI 결과에 따름**
- 상위 설계: `docs/MASTER_PLAN.md` 24장
- 선행: ADR-0001

## 문제

초기 GitHub CI는 Ubuntu만 검사했다. 또한 코드 계층의 import 금지와 AI 인계 JSON, 모듈 매니페스트, 개발 문서 장 번호의 정합성을 강제하지 않았다.

## 결정

1. 실행 환경과 UI 실기 검증을 분리한다. CI는 Windows+Ubuntu에서 기본 테스트만 수행한다.
2. 코드 경계는 AST 기반 정적 검사로 보호한다. 이는 완전한 정적 분석이나 동적 권한 제한이 아니다.
3. 인계·모듈 메타데이터는 JSON Schema Draft 2020-12로 검사한다.
4. 문서 검증은 마스터 장 순서·WO·상태 기록까지 검사한다.
5. 모듈은 아직 실행하지 않는다. Manifest는 계약 설계용이다.
6. 보안과 데이터 거버넌스는 별도 운영 문서로 기록한다.
7. WO-AGENT-01은 DRAFT로 미리 준비하며 WO-AGENT-00 GO 전에는 시작하지 않는다.
8. CI 성공을 실제 3개 CLI·Qwen·GPU·Qt 실행 증거로 해석하지 않는다.

## 제약과 남은 과제

- Windows runner는 사용자 PC가 아니므로 Win11 Snap·GPU·CLI 로그인 검증은 별도 필요하다.
- GitHub 브랜치 보호 설정은 별도 관리 작업이며 아직 확정하지 않았다.
- 플러그인 실행 격리·모델 LoRA 전환·외부 네트워크 검증은 해당 WO에서 구현한다.
- 외부 종속성과 CI action 업데이트는 보안·호환성 평가 후 진행한다.

## 검증

- `scripts/verify_project.py check`
- `scripts/check_architecture.py`
- `scripts/validate_contracts.py`
- `python -m unittest discover -s tests -v`
- GitHub Actions Windows/Linux 실제 수행 기록
