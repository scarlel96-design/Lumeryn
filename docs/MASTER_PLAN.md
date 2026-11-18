# Lumeryn 통합 마스터 설계서

> 문서 ID: SA-MASTER-001  
> 판본: **1.0.0 (최초 설계 기준)**  
> 기준일: **2026-11-18 (Asia/Seoul)**  
> 문서 상태: **설계안 / 구현 미완료**  
> 책임자: **사용자 = 제품 요구사항 및 주요 결정 승인 / Codex = 개발 총괄**  
> 원칙: 이 문서가 **제품 요구사항·아키텍처·개발 순서의 단일 기준 문서(Source of Truth)** 이다.

## 목차

1. 목적과 제품 정의
2. 범위·비범위·결정 현황
3. 불변 설계 원칙
4. 기능 요구사항과 우선순위
5. 전체 아키텍처 및 의존성 방향
6. 도메인·모듈·컴포넌트 경계
7. 경량 AI 코어·모델 관리
8. 검색·추론·인용 검증 파이프라인
9. 멀티모달 이미지·문서 처리
10. 정책 및 도구 권한 엔진
11. 전문 기능 플러그인·LoRA·전문 모델
12. 모델 파인튜닝·데이터 거버넌스
13. Windows 11 + Apple HIG 지향 UI/UX
14. API·이벤트·데이터 저장 계약
15. 신뢰 경계·보안·개인정보
16. 안정성·성능·관측 가능성
17. 테스트·평가·출시 게이트
18. Codex·Grok Build·Antigravity CLI 개발 운영
19. 개발 마일스톤·Work Order 로드맵
20. 작업 시작·종료·인계·변경 관리
21. 초기 환경·프로토타입 전환 계획
22. 기술적 위험·열린 결정·검증 필요 사항
23. 공식 참고 자료

---

## 1. 목적과 제품 정의

**Lumeryn**는 로컬 우선의 경량 **멀티모달 검색·추론 AI 플랫폼**이다. Qwen3.5-4B를 주력 모델로 사용한다. 기본 코어에는 실시간 웹 검색, 검색 계획, 근거 기반 추론, 이미지 검색 및 이미지 이해 기능이 포함된다. 전문적인 추가 기능은 설치형 모듈로 확장한다.

사용자는 모델의 동작 방식, 시스템 지침, 응답 형식, 안전·윤리 판단 규정, 응답 거부 기준 및 도구 사용 권한을 직접 관리한다. 이때 사용자 정책과 운영체제·외부 서비스의 필수 제한은 분리한다.

개발은 **모델 자체 개선(LoRA 등)** 과 **전용 Windows 프로그램 구축**을 함께 진행한다. 검색 기능의 향상은 모델 파라미터 증가가 아니라 검색 파이프라인과 평가로도 달성한다.

### 1.1 목표

- 주력 언어 모델은 **4B급**을 기준으로 유지한다. 새 기능을 위해 기본 가중치를 무조건 늘리지 않는다.
- 필요한 경우에만 도구 모듈, LoRA 어댑터 또는 독립 전문 모델을 적재한다.
- 정확한 검색어 생성, 질문 분해, 다중 검색, 재검색, 원문 검증을 지원한다.
- 텍스트·사진·차트·도면·스크린샷·PDF를 함께 분석한다.
- 원문 URL·문서 구간·이미지 영역과 최종 주장을 연결한다.
- 사용자 정의 정책을 버전별로 편집·검증·복원한다.
- Windows 11 고유 창 조작을 유지한다. 앱 내부 디자인은 iOS/macOS HIG 지향이다.
- Codex 총괄, Grok Build·Antigravity CLI 보조 운영으로 작업 시간·AI 사용량·재작업을 줄인다.
- 프로젝트의 현재 상태가 장기간 지나도 **저장소 파일만으로 복원**되도록 만든다.

### 1.2 성공의 정의

동일한 평가 데이터에서 검색·답변 정확도, 출처 인용 정확도, 사용자 제약 충족, 이미지 분석, 응답 시간, 메모리 사용량을 함께 평가한다. 목표는 특정 검색 작업에서 대형 상용 AI와 경쟁하는 것이다. 모든 분야의 일반 추론에서 동일한 성능을 보장하지 않는다.

### 1.3 비범위 / 하지 않을 일

- 첫 릴리스에서 다중 사용자 클라우드 서비스와 무제한 분산 학습을 개발하지 않는다.
- 모든 전문 분야를 주력 모델의 단일 가중치에 주입하지 않는다.
- 모델 출력을 진실 또는 보안 승인으로 취급하지 않는다.
- 실제 검증 없이 벤치마크·속도·AI 절감률을 주장하지 않는다.
- 초기 단계에서 완전한 멀티에이전트 개발 플랫폼을 제품 런타임에 탑재하지 않는다.
- Apple 브랜드 자산과 플랫폼 전용 폰트를 무단 배포하지 않는다.

## 2. 범위·비범위·결정 현황

| 결정 | 상태 | 내용 |
|---|---|---|
| 제품 형태 | 확정 | Windows 데스크톱 앱, 로컬 AI 백엔드 |
| 주요 모델 | 설계 채택 | Qwen3.5-4B, 이미지 입력 포함 |
| 핵심 기능 | 확정 | 검색·추론·출처 검증·이미지 검색/이해 |
| 확장 전략 | 확정 | Tool / LoRA / Specialist Model 3종 모듈 |
| 아키텍처 | 확정 | Clean + Layered + Ports & Adapters + Modular Monolith + SoC |
| 개발 AI | 확정 | Codex 메인, Grok Build와 Antigravity CLI 보조 |
| UI 방향 | 확정 | Win11 네이티브 창 버튼, 내부 Apple HIG 지향 |
| 모델 학습 | 설계 채택 | BF16 LoRA 우선, 실제 GPU 검사 필요 |
| 검색 구성 | 설계 채택 | SearXNG → 원문 수집 → 하이브리드 검색 → 검증 |
| 정책 처리 | 설계 채택 | 외부 정책 판정 엔진 + 도구 권한 게이트 |
| 배포·인증·업데이트 | 미확정 | 프로토타입과 PC 조사 후 세부 결정 |
| 성능·비용 수치 | 미검증 | 실제 기준 평가 이후 확정 |

**결정 상태 의미**: `확정`은 사용자 요구/아키텍처 방향, `설계 채택`은 구현 후보, `미확정`은 ADR 승인 필요, `미검증`은 실측 전을 뜻한다.

## 3. 불변 설계 원칙

### 3.1 Clean Architecture / Dependency Inversion

1. `domain`은 PySide6, Ollama, Qdrant, HTTP, SQL, Docker, LangGraph를 import하지 않는다.
2. `application`은 `domain`과 추상 `ports`에만 의존한다.
3. `infrastructure`는 `ports`를 구현한다. 코어는 외부 구현을 직접 인스턴스화하지 않는다.
4. `bootstrap/composition_root`가 구현체를 연결한다.
5. UI는 도메인 데이터 전달 객체(DTO)와 앱 서비스만 호출한다.
6. 저장소 의존성은 순환하지 않는다. 내부 패키지 전용 API를 다른 모듈이 직접 import하지 않는다.
7. 새 추상화는 실제 교체·테스트·확장 요구가 있을 때만 도입한다.

### 3.2 SoC·모듈화

- 모델 실행, 검색, 증거, 정책, 플러그인, 학습, UI, 저장을 각각 분리한다.
- 각 기능은 명시적인 계약·버전·오류·타임아웃을 갖는다.
- 기본 검색 코어를 활성 전문 모듈에 의존시키지 않는다.
- 전문 모듈을 비활성화하거나 제거해도 검색 코어는 정상 작동한다.
- 모델과 정책 버전은 프로그램 버전과 독립적으로 관리한다.

### 3.3 검증·변경 통제

- 작업마다 테스트 결과와 `PASS/FAIL/SKIP/NOT_RUN`을 구분한다.
- 새로운 라이브러리·모델·외부 서비스는 버전과 라이선스를 확인한다.
- 공개 API와 계약을 변경할 때는 ADR와 계약 테스트를 갱신한다.
- 모델 성능·학습 결과·실행 시간은 실제 로그로만 주장한다.
- 메인 브랜치·프로덕션 모델·실사용 정책의 변경은 최종 승인 단계를 거친다.

## 4. 기능 요구사항과 우선순위

우선순위: `P0` = 핵심 출시 필수, `P1` = 고도화, `P2` = 장기 확장. 구체적인 릴리스별 편성은 마일스톤과 WO로 결정한다.

### 4.1 기본 코어

| ID | 기능 | 우선 | 완료 조건의 예 |
|---|---|---|---|
| CORE-01 | 로컬 모델 실행·전환 | P0 | 원본/개발/Stable 분리와 모델 ID 기록 |
| CORE-02 | 한국어 채팅·구조화 출력 | P0 | 실제 모델 및 JSON 스키마 시험 |
| CORE-03 | 이미지 입력 | P0 | 픽셀 데이터 기반 이미지 분석 시험 |
| CORE-04 | 질문 의도·제약 추출 | P0 | 명시 조건 누락 없이 전달 |
| CORE-05 | 검색 계획·도구 호출 | P0 | 올바른 도구와 인수, 시간·예산 통제 |
| CORE-06 | SearXNG 등 실시간 검색 | P0 | 정상/빈 결과/오류 처리 |
| CORE-07 | HTML 원문 확보 | P0 | 실제 본문/URL/시간/해시 보존 |
| CORE-08 | 이미지 검색·수집 | P0 | 출처 있는 이미지 픽셀 분석 |
| CORE-09 | 근거 기반 답변 | P0 | 주장-원문 연결, 미확인 명시 |
| CORE-10 | 취소·타임아웃·복구 | P0 | 실행 중단 및 중복 실행 방지 |
| CORE-11 | 검색·모델·정책 실행 로그 | P0 | run_id와 버전으로 재현 가능 |
| CORE-12 | PDF·표·OCR | P1 | 페이지와 영역 추적 |
| CORE-13 | 하이브리드 검색·Reranker | P1 | Recall@K·latency 비교 |
| CORE-14 | 적응형 재검색·Deep Research | P1 | 정보 부족·예산·모순 분기 |
| CORE-15 | 주장 단위 인용 검증 | P1 | unsupported 주장 탐지 |

### 4.2 모델·정책·전문 모듈

| ID | 기능 | 우선 | 완료 조건의 예 |
|---|---|---|---|
| MODEL-01 | 모델 레지스트리·프로필 | P0 | 원본 보호·해시·호환성 |
| MODEL-02 | 시스템 프롬프트·생성 설정 | P0 | 프로필 별 저장·전환 |
| POL-01 | 사용자 정의 정책 | P0 | 버전·우선순위·충돌 처리 |
| POL-02 | 안전·윤리·거부 기준 편집 | P0 | 허용/거부/조건부/검토 판정 |
| POL-03 | 도구 권한 게이트 | P0 | 금지 명령 실행 방지 |
| MOD-01 | 모듈 계약·레지스트리 | P0 | 설치/활성화/비활성화 계약 |
| MOD-02 | 모듈 라우터·Lazy Load | P0 | 요청에 필요한 기능만 활성화 |
| MOD-03 | 자원·격리·권한 | P0 | RAM/VRAM/CPU·네트워크 제한 |
| MODEL-03 | LoRA 어댑터 관리 | P1 | 런타임/비전 호환성 검사 |
| MODEL-04 | 소형 전문 모델 적재 | P1 | 실행 후 메모리 회수 시험 |
| FT-01 | 검색·추론 LoRA | P1 | 원본 대비 평가 개선 |
| FT-02 | Vision SFT | P1 | 이미지 평가·일반능력 회귀 검사 |
| MOD-04 | 플러그인 SDK·마켓 | P2 | 공개 계약/서명/권한/롤백 |

### 4.3 Windows UI

| ID | 기능 | 우선 |
|---|---|---|
| UI-01 | Windows 11 닫기·최대화·최소화·Snap Layouts | P0 |
| UI-02 | Chat·Research Explorer | P0 |
| UI-03 | Model Studio·Policy Studio | P0 |
| UI-04 | Module Manager | P0 |
| UI-05 | Apple HIG 지향 디자인 시스템 | P0 |
| UI-06 | Spring/Connected Animation·Reduce Motion | P0 |
| UI-07 | Training Lab·Evaluation·Diagnostics | P1 |
| UI-08 | DPI·접근성·라이트/다크·반응성 | P0 |

## 5. 전체 아키텍처 및 의존성 방향

```text
[Windows Shell: Win11 native caption controls]
               |
[Presentation: PySide6/QML + optional FastAPI]
               |
[Application: Use Cases / State Machine / Budgets]
               |
[Domain + Ports: Pure Entities and Interfaces]
         ^           ^             ^
         |           |             |
[Adapters: Ollama][SearXNG/Qdrant][OPA/SQLite]
         ^
[Composition Root / Dependency Injection]

[Plugin Runtime] --calls--> [Public Capability Ports]
[Training Process] --produces--> [Versioned Adapter Artifacts]
```

의존성의 **코드 방향은 외부에서 내부로** 향한다. 위 세로 그림의 호출 흐름과 Python import 방향은 같지 않을 수 있다.

### 5.1 권장 저장소 구조

```text
Lumeryn/
├── AGENTS.md                         # 에이전트 필수 작업 지침
├── README.md
├── pyproject.toml                     # 생성 예정
├── apps/
│   ├── desktop/                      # PySide6 + Qt Quick/QML
│   └── api/                          # FastAPI / DTO
├── src/lumeryn/
│   ├── domain/                       # 순수 엔티티·검증 규칙
│   │   ├── model/ search/ evidence/ policy/ plugin/
│   ├── application/                  # 유스케이스·오케스트레이션
│   ├── ports/                        # LLM / Search / Storage / Policy / Plugin
│   ├── infrastructure/               # Ollama / SearXNG / Crawl4AI / Qdrant / OPA
│   └── bootstrap/                    # 의존성 조립
├── plugins/                          # 선택형 기능 모듈
├── module_sdk/                       # 모듈 계약·테스트 유틸
├── training/                         # 별도 환경의 학습·평가
├── devtools/orchestrator/            # 개발용 3중 AI Dispatcher
├── schemas/                          # JSON Schema·버전 계약
├── infra/                            # Docker·로컬 배포 설정
├── tests/unit/contract/integration/security/regression/
└── docs/                              # 마스터·현황·ADR·WO·실행 기록
```

초기에는 하나의 모듈형 모놀리스로 만든다. 고비용 수집기, 학습기 및 신뢰되지 않는 플러그인은 별도 프로세스로 격리할 수 있다.

## 6. 도메인·모듈·컴포넌트 경계

### 6.1 핵심 객체

- `ResearchRequest`: 질문·첨부·검색 모드·제약·정책 프로필
- `SearchIntent`: 의도·지역·기간·대상·필요한 근거 유형
- `SearchPlan`: 하위 질문·검색어·예산·정지 조건
- `SearchHit`: 검색원·URL·제목·발행일(알 수 없으면 null)
- `Document`: 정규화 URL·원문 해시·수집 시각·출처
- `Chunk`: 문서 내 구간과 원문 좌표
- `VisualEvidence`: 이미지 ID·원본·페이지·영역·관측 내용
- `Evidence`: 근거 ID·출처 구간·검증 결과
- `Claim`: 최종 답변 주장과 근거 매핑
- `PolicyDecision`: 허용/거부/조건부/승인/검토 및 규정 ID
- `ModuleManifest`: 기능·권한·자원·호환 버전
- `ModelManifest`: 베이스·어댑터·Tokenizer·Vision Processor·해시
- `ResearchRun`: 실행 ID·체크포인트·환경/모델/정책 버전

### 6.2 포트 계약

| 포트 | 최소 연산 | 주요 구현 |
|---|---|---|
| `LLMProvider` | chat, structured_output, analyze_image | Ollama, Transformers |
| `SearchProvider` | search(query, filters, budget) | SearXNG, 공식 API |
| `DocumentFetcher` | fetch(url, policy) | HTTP/Crawl4AI |
| `DocumentExtractor` | extract(bytes, mime) | HTML, PDF, OCR |
| `HybridRetriever` | index, retrieve | Qdrant 기반 구현 |
| `Reranker` | rank(question, candidates) | Qwen3-Reranker |
| `PolicyEvaluator` | evaluate(subject, action, context) | OPA, 로컬 규칙 |
| `ModuleRuntime` | activate, invoke, deactivate | Tool/LoRA/외부 프로세스 |
| `RunRepository` | save_checkpoint, load_run | SQLite |
| `TrainingBackend` | train, cancel, metrics | Unsloth 격리 실행 |

모듈 간 내부 클래스 직접 호출을 금지한다. 공개 포트/Capability Registry를 통해서만 협력한다.

## 7. 경량 AI 코어·모델 관리

### 7.1 기본 모델 정책

- 기본: **Qwen3.5-4B**. 정확한 원본 리비전과 해시를 저장한다.
- `Original`: 불변 원본. 평가의 기준.
- `Dev`: 실험 및 학습 대상.
- `Stable`: 검증을 통과해 승격한 모델.
- 로컬 추론은 Ollama를 우선 시험한다. 동적 LoRA 전환이 필요하면 별도 런타임 호환성을 평가한다.
- 모델 버전, Chat Template, Tokenizer, Vision Processor, Projector, 양자화와 API 지원을 별도로 기록한다.
- Qwen3.5 추론 모드는 실제 백엔드 API 옵션을 확인한다. 이전 Qwen3의 `/think`·`/nothink` 명령을 무조건 전용하지 않는다.
- 실제 VRAM이 확인되기 전까지 8K/16K/32K 컨텍스트를 단계별로 평가한다.

### 7.2 경량성 원칙

- 새 전문 기능 때문에 기본 LLM의 파라미터 수를 자동으로 늘리지 않는다.
- Type A: **Tool Module**—Python 도구·결정적 계산·외부 API.
- Type B: **LoRA Module**—기본 가중치는 보존하고 어댑터를 선택 적용.
- Type C: **Specialist Model**—작업 시에만 소형 전문 모델 적재.
- 모듈 추가로 디스크 사용량 또는 순간 RAM·VRAM이 늘 수 있다. 이를 모델 크기 유지와 혼동하지 않는다.
- Search Core 전용 LoRA의 변경도 독립 실험·승격 과정을 적용한다.

## 8. 검색·추론·인용 검증 파이프라인

1. **Request Validation**: 길이·형식·이미지 수·도구 권한 확인.
2. **Intent/Constraint Parsing**: 필수 조건·시간·지역·출력 요구 보존.
3. **Query Planning**: 하위 질문·검색원·쿼리·예산 결정.
4. **Search Brokerage**: SearXNG·선택적 공식 API·이미지 검색 호출.
5. **Fetch & Normalize**: 실제 원문·메타데이터·이미지 확보.
6. **Index & Hybrid Retrieve**: BM25 + Dense + RRF. Qdrant는 수집된 자료를 색인한다.
7. **Rerank & Compress**: 상위 근거만 모델에 전달. 증거 위치 보존.
8. **Evidence Check**: 원문 일치·모순·날짜·출처 품질 확인.
9. **Adaptive Re-search**: 부족하면 예산 내 추가 검색. 이유 기록.
10. **Synthesize**: 근거를 이용해 한국어 최종 분석 작성.
11. **Claim Validation**: 주장-출처 연결, 미확인/오래된 정보 표시.
12. **Policy Finalization**: 정책·권한·사용자 형식 점검.

검색 모드 예산은 초기 설계값이다.

| 모드 | 검색 호출(제안) | 목적 |
|---|---:|---|
| Fast | 1~2 | 간단한 최신 사실 |
| Balanced | 3~5 | 복수 출처 및 조건 검증 |
| Deep | 최대 20 | 다단계 조사·재검색·이미지 분석 |

검색 종료 조건: 필수 제약 충족, 근거 충분, 추가 검색 한계효용 감소, 예산 소진, 취소·오류. 예산 소진과 정보 미확인은 성공으로 포장하지 않는다.

### 8.1 인용 상태

`SUPPORTED`, `PARTIAL`, `CONTRADICTED`, `UNVERIFIED`, `OUTDATED`를 구별한다. `published_at`을 확인하지 못하면 `null`로 저장하고 수집 시각을 발행 시각으로 대체하지 않는다.

## 9. 멀티모달 이미지·문서 처리

- 웹 검색 결과에 이미지 설명만 전달하지 않는다. 실제 픽셀 데이터를 검증·전처리한 후 비전 모델에 제공한다.
- 원본 이미지 URL, 이미지가 있는 페이지 URL, MIME, 크기, 해시, 수집 시간을 보존한다.
- 사진·도면·차트·표·UI 스크린샷·스캔 PDF마다 분석 프롬프트와 검증 규칙을 구분한다.
- 작은 글자·부품 번호는 전체 이미지 분석 → 필요 영역 Crop/Zoom → 재분석 순서로 처리한다.
- PDF는 페이지 번호, 원문 구간, 이미지/표 영역을 기록한다.
- 모델의 시각 관측과 외부 원문의 사실 검증은 다른 상태로 저장한다.
- 추후 멀티모달 임베딩 모델(예: Qwen3-VL-Embedding)을 선택형 전문 모듈로 검토한다. 초기 필수 의존성은 아니다.
- 원본 이미지 보관·학습 사용에는 저작권·이용 조건과 개인정보 설정을 적용한다.

## 10. 정책 및 도구 권한 엔진

### 10.1 정책 계층

1. **Model Behavior**: 역할·성격·답변 스타일·검색 행동을 프롬프트 및 선택적 LoRA로 설정한다.
2. **User Policy**: 윤리·안전·응답 거부·예외·우선순위·검토 기준을 정책 파일과 UI에서 편집한다.
3. **Tool Enforcement**: 네트워크·파일·명령·모듈의 실제 실행 권한을 별도 게이트에서 판정한다.

정책 파일이 운영체제 보안이나 외부 API 약관을 무효화하지는 않는다. 모델의 학습된 응답 성향을 설정 파일만으로 완전히 제거할 수도 없다.

### 10.2 정책 결정

`ALLOW`, `ALLOW_WITH_CONDITIONS`, `REVIEW`, `REQUIRE_APPROVAL`, `DENY`. 각 결정은 규정 ID·버전·이유·요청 도구를 기록한다. 충돌 해결이 불가한 위험 작업은 실행하지 않는다.

### 10.3 정책 수명주기

Draft → Schema Check → Conflict Check → Simulated Tests → Approval → Active → Rollback. 정책 업데이트는 모델 가중치 변경과 분리한다.

## 11. 전문 기능 플러그인·LoRA·전문 모델

### 11.1 Module SDK 계약

필수: `module_id`, `version`, `capabilities`, `compatible_core`, `required_permissions`, `resource_limits`, `dependencies`, `entrypoint`, `health_check`, `lifecycle`, `uninstall_policy`.

```text
User Task -> Capability Router -> Policy Gate -> Module Registry
          -> Lazy Load/Start -> Execute -> Verify -> Unload/Stop
```

- Routing은 규칙 기반부터 시작한다. 모호한 요청에서만 LLM 판단을 사용한다.
- 모듈은 독립 설치·활성화·비활성화·업데이트·롤백·제거를 지원한다.
- 기본 검색 코어는 모듈이 전부 꺼져도 작동한다.
- LoRA 다중 합성은 기본으로 가정하지 않는다. 어댑터 호환성·성능을 개별 시험한다.
- 신뢰되지 않는 플러그인은 같은 Python 프로세스에 직접 로드하지 않는다.
- 오픈 API/SDK는 P2. 초기에는 내부 모듈 계약부터 안정화한다.

### 11.2 예비 전문 모듈 후보

Code Specialist, Math/Science, Document Analyst, Audio/ASR, Translation, Data Analysis, Automation. 후보는 기능 요구 시 우선순위를 재검토한다. 불필요한 모델을 상시 적재하지 않는다.

## 12. 모델 파인튜닝·데이터 거버넌스

### 12.1 학습 목표

- 최신 지식을 외우게 하기보다 **검색 전략·도구 호출·근거 추론·한국어 의도·이미지 읽기**를 개선한다.
- SFT/LoRA → 필요 시 Vision SFT → 필요 시 DPO/GRPO 순으로 진행한다.
- Qwen3.5-4B BF16 LoRA 요구 VRAM은 학습 시퀀스·이미지에 따라 변화한다. 공식 수치는 참고값이다.
- 4비트 추론과 BF16 학습을 구분한다. 모델 버전·Tensor/Processor 호환성을 평가한다.

### 12.2 데이터셋

- 분야: SEARCH_PLAN, TOOL_USE, EVIDENCE, REASONING, VISION, INSTRUCTION.
- 한 사례에 질문·제약·검색 계획·도구 흔적·실제 근거·검증 답·평가를 기록한다.
- 자동 생성 답변을 검증 없이 정답 데이터로 사용하지 않는다.
- 저작권·라이선스·개인정보·재배포 조건을 확인한다.
- 동일 원문·동일 사건의 파생 질문이 학습셋과 블라인드 평가셋에 동시에 들어가지 않도록 방지한다.
- 초기 계획상 14,000건은 확정 성능을 보장하는 최소량이 아니라 **장기 목표 후보**이다. 소규모 실험으로 수량을 조정한다.

### 12.3 실험·배포

- 원본 `L0`, 검색 LoRA `L1`, 근거 추론 `L2`, 혼합 `L3`, 비전 `L4`로 나누어 비교한다.
- 학습마다 `dataset manifest`, `base revision`, `config`, `seed`, `adapter`, `checkpoint`, `metrics`, `release decision`을 저장한다.
- 실패한 학습을 정식 모델에 적용하지 않는다.
- LoRA를 Ollama용으로 변환할 때 Vision Processor·Projector·Chat Template까지 실제 입력으로 검증한다.

## 13. Windows 11 + Apple HIG 지향 UI/UX

### 13.1 플랫폼 절충

- 닫기·최대화/복원·최소화는 **Windows 11 네이티브 방식**을 우선한다.
- Snap Layouts, Win+Z, 창 그림자, DPI, 키보드 및 멀티모니터 기능을 유지한다.
- 내부 레이아웃·질감·타이포그래피·간격·탐색·마이크로 인터랙션은 iOS/macOS HIG 수준의 경험을 지향한다.
- Apple 자체 리소스의 라이선스를 침해하지 않는다. 디자인 언어를 참고하고 배포 가능한 자산을 사용한다.

### 13.2 UI 구성

Chat, Research Explorer, Model Studio, Policy Studio, Module Manager, Training Lab, Evaluation & Diagnostics. 모든 화면은 공통 Design System과 ViewModel을 사용한다.

### 13.3 디자인 시스템

`Colors`, `Typography`, `Spacing`, `Radius`, `Elevation`, `Material`, `Motion`, `Iconography`, `Focus`, `Accessibility` 토큰을 별도 패키지로 둔다. QML 컴포넌트는 앱 로직에 직접 의존하지 않는다.

### 13.4 모션

- Spring/Smoothed Animation, Connected Transition, 상태 기반 Microinteraction을 지원한다.
- 초기 애니메이션 범위 100~400ms는 **설계 제안값**이다.
- 목표는 60FPS 이상의 부드러운 UI이며 실제 테스트 전 보장하지 않는다.
- Windows 모션 축소/애플리케이션 모션 축소를 지원한다.
- 애니메이션은 UI 스레드를 오래 차단하지 않는다. AI·검색·수집은 비동기로 실행한다.
- 투명도·블러·그림자는 GPU 사용량과 접근성을 고려해 선택적으로 적용한다.

## 14. API·이벤트·데이터 저장 계약

### 14.1 API v1 예시(제안)

`POST /v1/research/runs`, `GET /v1/research/runs/{id}`, `POST /v1/research/runs/{id}/cancel`, `GET /v1/research/runs/{id}/events`, `GET /v1/models`, `POST /v1/models/activate`, `GET /v1/policies`, `POST /v1/policies/validate`, `POST /v1/policies/activate`, `GET /v1/modules`, `POST /v1/modules/{id}/activate`, `POST /v1/training/jobs`, `POST /v1/evaluations/runs`, `GET /v1/system/health`.

각 요청에는 `request_id`를 부여한다. 오류에는 `code`, `message`, `retryable`, `details`를 포함한다. 외부 API와 내부 Domain 객체는 직접 공유하지 않고 DTO로 변환한다.

### 14.2 저장 계층

- SQLite: 설정·정책·대화·실행·감사·평가 메타데이터.
- Qdrant: 검색 문서의 Dense/Sparse 벡터 색인.
- 로컬 Object Store: 원문·이미지·학습 데이터·어댑터.
- 모델 가중치·대형 데이터셋·비밀값은 Git 저장소에 커밋하지 않는다.
- `run_id` → 모델·엔진·정책·데이터 버전으로 추적 가능해야 한다.
- 사용자 대화 기억, 사용자 선호, 수집 문서 기억은 별도로 저장·삭제·갱신한다.

## 15. 신뢰 경계·보안·개인정보

- 외부 웹페이지와 이미지, 플러그인 설명, LLM 출력은 신뢰되지 않는 데이터이다.
- 프롬프트 주입을 시스템 지침으로 승격하지 않는다.
- URL 접근에 대해 SSRF·리다이렉트·DNS 재바인딩·내부 IP·클라우드 메타데이터를 방어한다.
- 네트워크 격리는 문자열 필터보다 강한 수준으로 적용한다.
- 도구 이름·스키마·인수·크기·횟수·권한·승인 상태를 실행 전에 검사한다.
- API 키·사용자 비밀값은 코드·학습 데이터·모델 입력에서 분리한다.
- 외부 AI 에이전트에 사용자의 기밀 데이터나 API 키를 무심코 전달하지 않는다.
- 정책·모델·플러그인 업데이트에 해시 검증·호환성 검사·롤백을 적용한다.
- 실패 시 위험 작업은 기본 차단한다. **읽기 전용 진단과 실제 쓰기 작업**을 구분한다.
- 외부 서비스 약관·수집 자료의 저작권 및 학습 이용조건을 준수한다.

## 16. 안정성·성능·관측 가능성

- LangGraph 체크포인트는 중간 상태를 저장한다. 외부 쓰기 작업은 별도 멱등성 키가 필요하다.
- 상태: CREATED → VALIDATING → PLANNING → SEARCHING → FETCHING → VERIFYING → SYNTHESIZING → FINAL_CHECK → COMPLETED.
- 예외: RETRYABLE_ERROR, WAITING_FOR_APPROVAL, CANCEL_REQUESTED, CANCELLED, TIMEOUT, FAILED, HOLD.
- 검색 모드별 시간·도구 호출·원문 수·이미지 수 예산을 설정한다.
- GPU 작업은 `GPU Lock`을 사용한다. 학습과 대규모 추론의 중복 실행을 초기에는 금지한다.
- 로그에는 정답을 꾸며 넣지 않는다. `PASS`, `FAIL`, `SKIP`, `NOT_RUN`을 엄격히 구분한다.
- 성능은 p50/p95 지연시간, Peak VRAM/RAM, 검색 예산, 성공률, 재시도 횟수로 측정한다.

## 17. 테스트·평가·출시 게이트

### 17.1 테스트 수준

- Unit: 외부 서비스 없이 단일 컴포넌트 테스트.
- Contract: 모든 SearchProvider/LLMProvider/ModuleRuntime 어댑터가 공통 계약을 만족하는지 테스트.
- Integration: SearXNG·Ollama·Qdrant 등 실제 연결 확인.
- E2E: 사용자 질문부터 출처 있는 답변까지 검증.
- Security: SSRF, 권한 위반, 프롬프트 주입, 플러그인 격리.
- Regression: 모델·검색·UI·정책 수정 전후 비교.
- Architecture: 순환 의존성, 금지 import, 코어와 UI 분리 검사.

### 17.2 평가셋

초기 설계값은 500문항: 일반 사실 100, 최신 정보 100, 다단계 추론 100, 이미지·도표 100, 복잡한 제약 50, 정책·권한 50. 개발·검증·블라인드 테스트로 나눈다. 실제 구성과 점수 목표는 베이스라인 이후 결정한다.

지표: Recall@20, Precision@5, 정답 정확도, 사용자 제약 충족, 출처-주장 연결, 이미지 분석 정확도, 적절한 답변 보류, 지연시간, 자원 사용량, 정책 준수.

### 17.3 출하 판정

- **GO**: 필수 계약·테스트 통과, 치명적 보안·데이터 결함 없음, 요구사항·호환성·릴리스 증거 확보.
- **HOLD**: 필수 통합 시험 미실시 또는 미확인 종속성 존재.
- **NO-GO**: 실제 실패한 필수 테스트, 데이터 손상, 권한 우회, 정식 모델 회귀 등 출시 차단 문제 존재.

미실시 테스트를 PASS로 계산하지 않는다. 목표치를 달성하지 못한 상태를 성공으로 선언하지 않는다.

## 18. Codex·Grok Build·Antigravity CLI 개발 운영

### 18.1 역할

- **Codex (Lead)**: 기술 의사결정 제안, Work Order 분해, 공통 계약, 핵심 구현, 리뷰, 통합·릴리스 판정.
- **Grok Build**: 승인된 독립 모듈 구현, 테스트 생성, 다른 관점의 코드 리뷰.
- **Antigravity CLI**: 기술 호환성 조사, Qwen/Unsloth·Qt/Windows 등 실험 지원, 독립 검토.
- **User**: 범위·비용·외부 권한·주요 변경·정식 배포 승인.

### 18.2 효율 규칙

- 기본은 **Codex 단독**. 병렬이 시간과 재작업을 줄이는 경우에만 보조를 투입한다.
- 기본 병렬 상한은 Codex/Grok/Antigravity 각 1세션이다. 하위 에이전트 중첩은 기본 금지.
- 파일 쓰기를 수행하는 보조 에이전트는 별도 Git Worktree를 사용한다.
- 공통 코드 계약은 Codex가 먼저 확정한다. 계약 미확정 작업에 보조 구현을 병렬로 투입하지 않는다.
- 단순한 검사는 pytest·ruff·mypy 같은 일반 도구로 먼저 수행한다.
- 성공 조건은 **프로세스 종료 + 실제 변경·산출물 + 테스트**의 결합이다.
- CLI는 공급자별 사용량 형식이 다르다. 임의로 총 토큰을 합산하지 않는다.
- 사용자 승인 없이 외부 Git push, 배포, 결제, 비밀정보 전송을 하지 않는다.
- 에이전트 출력은 보고서이지 검증 증거 자체가 아니다.

### 18.3 파일과 시작 규칙

모든 새 세션 및 모든 WO의 작업 시작 전에, **`AGENTS.md` → `docs/MASTER_PLAN.md` 전체 → `docs/PROJECT_STATE.md` → 해당 WO → 관련 ADR → 관련 코드** 순으로 읽는다. 대화 기억이나 이전 요약만으로 작업을 시작하지 않는다. `scripts/verify_project.py`로 필수 파일·WO 상태·해시를 검사한다.

**주의**: 스크립트는 파일 무결성과 실행 기록을 확인하지만, 에이전트가 문서를 실제로 이해했는지 자동 보증하지 못한다. 에이전트는 시작 보고에 기준 문서 SHA-256, 현재 작업, 관련 장·제약, 선행조건을 요약해야 한다.

## 19. 개발 마일스톤·Work Order 로드맵

### M0 — 3중 AI 개발 환경과 거버넌스 (가장 먼저)

- `WO-AGENT-00`: Codex/Grok/Antigravity 설치·인증·권한·문서 읽기·작업 분리·결과 인계·실패 판정 실증.
- `WO-AGENT-01`: 경량 Dispatcher, WO 검증, Git Worktree, 사용량 측정, 작업 상태 머신.
- Gate: 세 CLI 실행 여부의 실제 증거와 불필요한 AI 호출 없이 복구 가능한 절차.

### M1 — 모델·제품 기반

- `WO-01`: CPU/GPU/VRAM/RAM/드라이버/WSL2 환경 조사.
- `WO-02`: 원본 Qwen3.5-4B 텍스트·도구·비전 기준 평가.
- `WO-03`: Clean Architecture 프로젝트·CI·공통 계약·테스트 기반.
- `WO-04`: Ollama 추론 어댑터·이미지 입력·구조화 출력.
- `WO-05`: 모델 레지스트리·프롬프트 프로필·버전 관리.
- `WO-MOD-01`: Module SDK 공개 계약·기본 Registry 골격.

### M2 — 기본 검색 코어

- `WO-06`: 기본 정책 엔진·허용/거부/승인 게이트.
- `WO-07`: SearXNG 검색 어댑터.
- `WO-08`: 의도 분석·검색 계획·제약 보존.
- `WO-09`: Crawl4AI/HTML/PDF 원문 수집.
- `WO-10`: 이미지 검색·수집·안전 전처리.
- `WO-11`: SQLite/문서 해시/근거 저장소.
- `WO-12`: Qdrant Hybrid Retrieval.
- `WO-13`: Qwen Embedding/Reranker 연동.

### M3 — 정밀 추론·정책·UI·플러그인

- `WO-14`: 주장 단위 근거·인용 검증.
- `WO-15`: LangGraph 재검색·중단·체크포인트.
- `WO-16`: 이미지·차트·스크린샷·PDF 멀티모달 통합.
- `WO-17`: Policy Studio·OPA·충돌·버전 관리.
- `WO-18`: Model Studio·어댑터 관리자.
- `WO-MOD-02`: 모듈 설치/활성화/권한/자원/라우터.
- `WO-UI-01`: Win11 네이티브 창 프레임·Snap 테스트.
- `WO-UI-02`: Apple HIG 지향 Design System·QML 공통 컴포넌트.
- `WO-UI-03`: Spring/Connected Motion·Reduce Motion·DPI·접근성.
- `WO-19`: Chat/Research/Modules/Training/Diagnostics 화면 통합.

### M4 — 안정판·평가

- `WO-20`: 평가셋·벤치마크 실행기·회귀 검증.
- `WO-21`: 보안·성능·오류 복구 통합 검증.
- `WO-22`: 첫 Stable Release GO/HOLD/NO-GO 판정.

### M5 — 모델 학습 고도화 (데이터 수집은 M1부터 병행 가능)

- `FT-01`: 데이터 거버넌스·검색 사례·훈련/검증/테스트 분리.
- `FT-02`: 검색 계획·도구 호출 LoRA.
- `FT-03`: 근거 추론·한국어 분석 LoRA.
- `FT-04`: Vision SFT·모듈/일반능력 회귀.
- `FT-05`: DPO 후보 실험(효과 있을 때만).
- `FT-06`: GRPO 후보 실험(객관 보상 설계 후).

### M6 — 배포

- `REL-01`: 모델·Vision Processor·GGUF 및 런타임 호환성 확인.
- `REL-02`: Windows 설치/제거·백업·복원·코드 서명 검토.
- `REL-03`: 해시·호환성·트랜잭션 업데이트·롤백.

### 의존성 핵심

`M0 → M1 → M2 → M3 → M4 → M6`. `FT-01` 준비는 M1부터 가능하지만, 본격 FT-02~04 승격은 M4의 기준 평가 체계가 필요하다. Module SDK는 검색 엔진을 완성한 뒤 덧붙이지 않는다. UI 공통 디자인 시스템은 화면 구현보다 먼저 만든다.

작업별 실제 시작·완료·보류 상태는 **`docs/PROJECT_STATE.md`만** 편집한다. 계획 항목 자체를 변경할 때는 본 문서와 ADR를 함께 수정한다.

## 20. 작업 시작·종료·인계·변경 관리

### 20.1 매 WO 필수 시작 절차

1. 저장소 루트에서 `AGENTS.md`를 읽는다.
2. `docs/MASTER_PLAN.md` **전체**를 읽는다. 일부 발췌·이전 대화 요약으로 대체하지 않는다.
3. `docs/PROJECT_STATE.md`를 읽고 현재 상태를 검증한다.
4. 해당 `docs/WORK_ORDERS/<WO-ID>.md`를 읽는다.
5. 적용되는 ADR·정책·인터페이스·테스트 문서를 확인한다.
6. `python scripts/verify_project.py check --wo <WO-ID>`로 파일·참조·해시를 검사한다.
7. 시작 보고: `master_sha256`, 현재 단계, 선행조건, 담당자, 변경 허용 경로, 검증 계획, 충돌 위험을 명시한다.
8. 선행조건 미충족, 문서 불일치 또는 작업 범위 불명확 시 코드 변경을 시작하지 않고 HOLD로 보고한다.

### 20.2 매 WO 필수 종료 절차

1. 소스 코드와 실제 테스트 결과를 기록한다.
2. 변경 파일·커밋·환경·모델·정책 버전을 기록한다.
3. `docs/PROJECT_STATE.md`의 현재 상태와 다음 작업을 갱신한다.
4. 설계 변경이 발생했다면 ADR/마스터 문서 판본을 갱신한다.
5. 최종 보고: `PASS/FAIL/SKIP/NOT_RUN`, 미해결 문제, 다음 선행조건.
6. Codex가 전체 병합·완료·출시 판정을 담당한다.

### 20.3 계획 변경 절차

요구사항 변경 → 변경 영향 분석 → ADR 작성 → 사용자 또는 승인권자의 결정 → `MASTER_PLAN` 새 버전 → 관련 WO/계약 갱신 → 회귀 테스트. 기존 승인 기록을 삭제하지 않는다. 변경 전 버전은 Git에서 추적한다.

## 21. 초기 환경·프로토타입 전환 계획

기존에 생성된 `SearchAI-Starter-0.1.0.zip`은 **기초 프로토타입**으로 간주한다. 새 마스터 설계서나 모듈형 Clean Architecture 구현체로 간주하지 않는다.

이전 프로토타입의 설명상 구현: Ollama 텍스트/선택적 이미지, SearXNG 검색, 단순 RRF 병합, 기본 HTML 추출, JSON 도구 정책, 모의 단위 테스트. 그 기록의 실제 설치·실행·서비스 동작은 새 PC 환경에서 재검증해야 한다.

통합 원칙:

1. 원본 소스와 기존 테스트를 읽고 유용한 기능만 선별한다.
2. 핵심 도메인 계약을 우선 만든 뒤 기존 구현을 어댑터로 분리한다.
3. 프로토타입을 검증 없이 덮어쓰거나 정식 구현으로 승격하지 않는다.
4. 전환 과정에서 동작 유지 테스트를 작성한다.
5. 필요하면 새 저장소에 마스터 설계 문서를 먼저 추가한 후 점진적으로 마이그레이션한다.

## 22. 기술적 위험·열린 결정·검증 필요 사항

| 항목 | 현재 상태 | 검증 시점 |
|---|---|---|
| 실제 GPU VRAM·RAM | 미확인 | WO-01 |
| BF16 LoRA 로컬 가능성 | 미확인 | WO-01/FT-01 |
| Qwen3.5-4B 도구/비전 정확도 | 미측정 | WO-02 |
| LoRA Vision 배포 호환 | 미측정 | FT-04/REL-01 |
| SearXNG 실제 검색 성공률 | 미측정 | WO-07 |
| Qt Win11 Snap 커스텀 크롬 | 설계 대안 필요 | WO-UI-01 |
| 3개 CLI 설치·인증·사용량 | 미검증 | WO-AGENT-00 |
| 병렬 AI 작업시간 절감률 | 미측정 | WO-AGENT-01 이후 |
| 외부 검색 API 필요성·요금 | 미결정 | WO-07/WO-20 |
| 학습 데이터 14,000건 타당성 | 가설 | FT-01 |
| 정확도 대형 모델 대비 | 미검증 | WO-20 이후 |
| 플러그인 격리 방식 | 미결정 | WO-MOD-02 |
| 첫 정식 배포 형식·라이선스 | 미결정 | REL-02 |

결정이 필요한 항목은 임의로 확정하지 않는다. 사용자에게 불필요한 질문을 반복하기보다, 확인 가능한 사실을 먼저 조사하고 안전한 임시 기본값을 표시한다.

## 23. 공식 참고 자료

아래는 **공식 또는 1차 기술 문서**의 주요 주소이다. 현재 버전과 라이선스는 해당 WO의 시작 시 다시 확인한다.

- Qwen3.5-4B: https://huggingface.co/Qwen/Qwen3.5-4B
- Ollama: https://ollama.com/library/qwen3.5 / https://docs.ollama.com/api
- Unsloth Qwen3.5: https://docs.unsloth.ai/models/qwen3.5/fine-tune
- LangGraph 지속성: https://docs.langchain.com/oss/python/langgraph/persistence
- SearXNG Search API: https://docs.searxng.org/dev/search_api.html
- Crawl4AI: https://docs.crawl4ai.com/
- Qdrant Hybrid Search: https://qdrant.tech/documentation/
- OPA: https://www.openpolicyagent.org/docs
- Qt Quick Animation: https://doc.qt.io/qt-6/qtquick-statesanimations-animations.html
- Apple HIG: https://developer.apple.com/design/human-interface-guidelines/
- Microsoft Windows 앱 창: https://learn.microsoft.com/windows/apps/develop/title-bar
- Codex AGENTS/장기 작업: https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex
- Codex ExecPlan: https://developers.openai.com/cookbook/articles/codex_exec_plans
- Grok Build: https://docs.x.ai/build/overview
- Grok AGENTS 규칙: https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/12-project-rules.md
- Antigravity CLI 규칙: https://antigravity.google/docs/cli/best-practices/
- Antigravity Rules: https://antigravity.google/docs/rules/

**문서 유지 지침**: 장기 개발 중 새로운 결정은 이 문서를 조용히 덮어쓰지 않는다. ADR 번호와 변경 사유, 영향 받는 WO, 검증 방법을 기록하고 버전을 올린다.