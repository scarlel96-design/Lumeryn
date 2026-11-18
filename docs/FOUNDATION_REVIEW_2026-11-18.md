# Lumeryn 기초 개발 기반 정밀 점검 보고서 — 2026-11-18

> 범위: `main`의 초기 설계/코드와 이번 hardening PR의 변경 내용.
> 목적: 개발 착수 전에 단절된 계약, 장기 상태 망각, 보안/성능의 미검증 구역을 명확히 한다.
> **코드/문서 기반 평가**다. 사용자 Windows PC의 CLI 로그인, 모델 학습과 GUI 동작 시험은 포함하지 않는다.

## 1. 원본 저장소 조사 결과

초기 저장소에는 23개 장의 마스터 설계서, `AGENTS.md`, `PROJECT_STATE.md`, 첫 WO, Python 계약 골격, Ubuntu CI가 있었다.
초기 도메인 모델은 `ResearchQuery`, `SearchHit`, `ResearchSnapshot`이다.
`RetrieveCandidates`는 `SearchProvider`를 주입받는 골격이며 실제 검색/LLM 요청을 수행하지 않는다.

## 2. 발견 사항·조치 결과

| ID | 위험도 | 발견 사항 | 이번 보강 | 남은 작업 |
|---|---|---|---|---|
| FND-01 | P0 | 마스터 번호 중복/문서 불일치 검출 부족 | 설계서 장 순서/파일/WO 검증 강화 | 실제 세션 시작 보고 검토 |
| FND-02 | P0 | Clean Architecture 금지 import 검사 없음 | AST 기반 금지 import 및 cycle 검사 | 동적 import/전체 종속성 검사 |
| FND-03 | P0 | AI 인계 JSON을 자동 검증하지 않음 | JSON Schema, 현재 마스터 해시, 완료 상태 검사 | 실제 Git/로그와 대조 |
| FND-04 | P0 | CI가 Ubuntu 단일 플랫폼 | Windows+Ubuntu matrix, 읽기 권한 제한 | 실제 Win11 UI·GPU·권한 시험 |
| FND-05 | P0 | 임의 전문 모듈의 규격 미정 | Type A/B/C용 모듈 매니페스트 | 실행 격리·서명·로드/언로드 |
| FND-06 | P0 | 도구 실행·외부 검색 신뢰 경계 설명 부족 | 별도 위협 모델·실행 통제 명세 | 실제 SSRF/프롬프트 주입 시험 |
| FND-07 | P1 | 개인 대화·웹 근거·학습 데이터 구분 부족 | 데이터 거버넌스·라이선스·승격 규칙 | 저장소/개인정보 삭제 구현 |
| FND-08 | P1 | 원본·개발·정식 모델 버전 계약 없음 | 모델 매니페스트 및 STABLE 조건 | 실제 원본 revision/해시 확보 |
| FND-09 | P1 | 사용자 정책 설정 예제의 실행 계약 부재 | 비활성 정책 메타데이터 스키마 | Policy Gate·OPA/정책 충돌 검사 |
| FND-10 | P1 | 문서 링크가 깨져도 CI 성공 | 상대 링크 존재 검사 | 외부 URL/앵커 검증은 향후 |
| FND-11 | P1 | 다음 3중 AI 작업 WO 초안 없음 | WO-AGENT-01 DRAFT 준비 | WO-AGENT-00 GO 후 승인 |
| FND-12 | P1 | Windows용 시작 절차가 단편적 | 읽기 전용 inventory/WO 프리플라이트 | 실제 Windows PC에서 실행 |
| FND-13 | P1 | AI 고급 협업 시 감사가 어려움 | PR 템플릿·인계 표준·운영 규칙 | Dispatcher 실측 로그 |
| FND-14 | P1 | Win11 네이티브 UI와 Apple HIG 수락 기준 분산 | 별도 UI 테스트 명세 | Win11 실제 표시·모션 시험 |
| FND-15 | P1 | 경량/검색 비용 목표에 계측 계약 미흡 | 성능 예산 문서 | 실제 PC 베이스라인·모델 비교 |
| FND-16 | P2 | GitHub `main` 보호 규칙 여부 미확정 | PR 기반 운영 권고 | 별도 GitHub Settings 확인 |
| FND-17 | P2 | 종속성·모델 공급망 잠금 파일 없음 | 업데이트 위험 문서화, Action SHA 핀 | 이후 의존성 lock/SBOM 설계 |
| FND-18 | P2 | 전체 검색·이미지·LoRA 통합 시험 없음 | 평가/증거 기준 명확화 | M1~M6 제품 WO에서 구현 |

## 3. 실행 검증 범위

기본 CI는 GitHub Actions에서 다음을 확인한다.

1. Python 패키지 설치 및 기본 오프라인 테스트.
2. 설계서·상태·WO 존재와 마스터 장 순서.
3. Domain/Application 정적 import 경계 및 직접 import cycle.
4. 인계/모듈/모델/정책 JSON Schema의 예시 유효성.
5. 내부 Markdown 링크와 Python 문법.
6. Windows runner 및 Ubuntu runner 결과.

**다음 시험은 아직 실행하지 않았다.**

- 실제 사용자 PC의 Codex·Grok Build·Antigravity CLI 로그인/권한/Worktree.
- Qwen3.5-4B 텍스트·이미지·도구 호출.
- Windows 11의 Snap Layouts, Narrator, 100~200% DPI, Spring Animation.
- SearXNG/Crawl4AI/Qdrant 실제 검색 및 SSRF 격리.
- Unsloth BF16 LoRA, GGUF export, Vision Processor 호환성.
- 실제 성능 목표, 비용·토큰 절감률.

## 4. 누락을 다시 만들지 않기 위한 규칙

- GitHub 트리·커밋 작성 시 **직전 브랜치 HEAD의 Tree SHA**를 기준으로 사용한다.
- 이전 커밋에만 있던 파일이 후속 커밋에서 사라지지 않았는지 `git diff --name-status`와 전체 트리 비교로 확인한다.
- 각 PR은 모든 계획된 파일이 남아 있는지와 현재 마스터 해시를 검증한다.
- CI에서 일부 시험이 PASS여도 명시된 실기 시험이 NOT_RUN이면 WO 완료로 전환하지 않는다.
- `WO-AGENT-01`은 명세만 DRAFT로 유지한다.

## 5. 다음 작업의 순서

1. 이번 보강 PR 전체 CI와 파일 트리 확인.
2. Codex가 PR 변경과 안전성을 검토하고 승인된 내용을 `main`에 반영.
3. 사용자 PC에서 `WO-AGENT-00`을 시작. 문서 전체 읽기·지침·CLI/인증/격리 실측.
4. 결과·실제 커밋·로그를 `PROJECT_STATE.md`에 기록하고 GO/HOLD/NO-GO 판정.
5. GO 이후 `WO-AGENT-01` Dispatcher 작업지시서를 확정하고 구현.
6. 모델 하드웨어 조사 및 원본 Qwen 평가를 거쳐 검색 코어와 UI 개발에 착수.

## 6. 공식 참고

- GitHub Branch Protection: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- OWASP Prompt Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
- OWASP LLM Top 10: https://genai.owasp.org/llm-top-10/
- Python Packaging: https://packaging.python.org/en/latest/

## 7. 판정

- **설계·기초 검사 체계:** CI PASS 확인 후 통합 가능.
- **사용자 PC의 3중 AI 협업 기반:** 아직 WO-AGENT-00 READY.
- **Lumeryn 검색/멀티모달/파인튜닝 제품:** NOT_IMPLEMENTED/NOT_RUN.
