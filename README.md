# Lumeryn

**Lumeryn**은 Qwen3.5-4B 기반의 로컬 우선 멀티모달 검색·추론 AI 플랫폼을 목표로 하는 개발 프로젝트입니다.

> **현재 상태:** 설계/개발 초기 골격. 검색 엔진, AI 모델 연결, GUI, LoRA 학습은 아직 완성되지 않았습니다.

## 핵심 목표

- 기본 검색 코어: 웹 검색, 질문 분해, 이미지 이해, 근거·인용 검증
- 고정형 경량 주력 모델 + 선택적 Tool / LoRA / Specialist Model 모듈
- Clean Architecture · Ports & Adapters · SoC · Modular Monolith
- Windows 11 네이티브 창 버튼과 Snap 동작, 내부는 Apple HIG 지향 UI·모션
- 사용자 정의 시스템 지침, 안전·윤리·거부·도구 실행 정책
- 모델 학습·검색 엔진·UI·플러그인의 독립적인 개발·검증·업데이트
- Codex 총괄, Grok Build·Antigravity CLI 선택적 보조

## 반드시 읽을 문서

| 문서 | 용도 |
|---|---|
| [AGENTS.md](AGENTS.md) | 매 작업 시작 시 모든 AI가 지켜야 할 규칙 |
| [MASTER_PLAN.md](docs/MASTER_PLAN.md) | **전체 개발의 최상위 설계서(23개 장)** |
| [PROJECT_STATE.md](docs/PROJECT_STATE.md) | 현재 상태·완료/보류 작업·다음 WO |
| [WORK_ORDER_INDEX.md](docs/WORK_ORDER_INDEX.md) | 단계별 WO·의존성·AI 배정 |
| [WO-AGENT-00](docs/WORK_ORDERS/WO-AGENT-00.md) | 첫 번째 실제 작업 |
| [첫 실행 가이드](docs/DEVELOPMENT_START.md) | 설치·문서 검증·작업 전달 순서 |
| [AI별 작업지시서](docs/PROMPTS/) | Codex → Grok/Antigravity → Codex |
| [아키텍처 요약](docs/ARCHITECTURE.md) | 모듈/레이어 책임과 교체 경계 |
| [완료 기준](docs/ACCEPTANCE.md) | 테스트와 GO/HOLD/NO-GO |
| [요구사항 추적](docs/REQUIREMENTS_TRACEABILITY.md) | 기능 누락 추적 |

## 첫 개발 시작

```powershell
git clone https://github.com/scarlel96-design/Lumeryn.git
cd Lumeryn
py -3.12 scripts/verify_project.py check --wo WO-AGENT-00
py -3.12 -m unittest discover -s tests -v
```

첫 WO 지시서는 [01-CODEX-START.md](docs/PROMPTS/01-CODEX-START.md)입니다. **Codex가 작업 공간을 준비한 후에만** 두 보조 AI를 투입합니다.

## 패키지 골격

- `src/lumeryn/domain/`: 외부 라이브러리에 종속되지 않는 도메인 모델
- `src/lumeryn/application/`: 유스케이스와 추상 포트
- `src/lumeryn/infrastructure/`: 향후 Ollama·검색·저장소 구현
- `apps/desktop/`: 향후 PySide6 + QML Windows 앱
- `plugins/`: Tool·LoRA·전문 모델 플러그인
- `training/`: 독립 학습 파이프라인
- `devtools/`: 3중 AI 개발 작업 분배기(미구현)

현재 Python 코드는 **외부 호출 없는 계약 골격**만 제공합니다. 본문 웹 검색·LLM 답변이 가능한 제품이라고 주장하지 않습니다.

## 작업 운영 원칙

모든 개발 AI는 **매 새 WO·세션 시작 시 `AGENTS.md`와 `docs/MASTER_PLAN.md` 전체를 읽고**, 상태와 WO를 확인합니다. 변경 전 설계서·현재 상태·수정 범위를 검증합니다. 완료 시 `PROJECT_STATE.md`와 실제 테스트 증거를 갱신합니다.

외부 배포, 무제한 권한 부여, 비밀정보 전송, 제품 모델의 무검증 교체는 금지합니다.

## 시작 배포 내용

- 기존 Blueprint 1.0 문서를 **Lumeryn 명칭으로 이식**
- 초기 Python 패키지 구조와 계약 기반 Research 유스케이스
- 문서 검증 스크립트·단위 테스트
- GitHub Actions 최소 CI
- 향후 기능용 플레이스홀더 및 작업 지침

정식 프로그램의 동작 여부, GPU 성능, 세 CLI의 실제 인증·연동 결과는 아직 검증되지 않았습니다.

## Foundation hardening (planned integration)

개발 장기 운영·품질 게이트 보강 내용은 별도 PR에서 검증한다.
- [보안 위협 모델](docs/SECURITY_MODEL.md)
- [데이터 거버넌스](docs/DATA_GOVERNANCE.md)
- [모듈 계약](docs/MODULE_CONTRACTS.md)
- [장기 개발 상태·인계 절차](docs/OPERATIONS_AND_STATE.md)
- [차기 Dispatcher WO 초안](docs/WORK_ORDERS/WO-AGENT-01.md)

정적 계약·메타데이터 검증은 실제 AI 기능 구현 또는 모델 학습이 아니다.
