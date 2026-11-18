# Lumeryn Module SDK 초기 계약 — v1 설계

> **메타데이터와 검증 준비만 완료. 동적 플러그인 실행 기능은 아직 없음.**

## 1. 모듈 유형

| 유형 | 역할 | 기본 모델 크기 | 실행 자원 |
|---|---|---|---|
| Tool Module | 결정적 계산, 파일 변환, API | 유지 | 코드·프로세스 자원 |
| LoRA Module | 기존 4B 모델 전문화 | 기본 가중치 유지 | 어댑터 적재 메모리 |
| Specialist Model | 음성/비전/특수 임베딩 | 주력 모델 유지 | 별도 모델 메모리 |

검색·이미지 이해·근거 검증은 기본 코어다. 전문 모듈이 모두 비활성화되어도 기본 검색은 사용 가능해야 한다.

## 2. 표준 계약

초기 JSON Schema: `schemas/module-manifest.schema.json`.

필수: `schema_version`, `module_id`, `version`, `kind`, `capabilities`, `compatible_core`, `permissions`, `resources`, `activation`.

- `kind=tool`: `entrypoint` 필수. 현재는 메타데이터만 검증하고 실행은 금지한다.
- `kind=lora`: `base_model` 필수. 원본 모델과 Tokenizer·Vision Processor 호환성이 별도 필요하다.
- `kind=specialist_model`: 모델 매니페스트와 실행 백엔드 검증이 추가로 필요하다.
- `permissions`: 네트워크, 파일시스템, 외부 명령 등 위험 능력을 명시한다.
- `activation`: 초기값은 비활성화·지연 적재가 권장된다.

예제: `plugins/examples/math-tool/manifest.json`.

```powershell
py -3.12 -m pip install -e ".[dev]"
py -3.12 scripts/validate_contracts.py module plugins/examples/math-tool/manifest.json
```

## 3. 설계 원칙

1. Module SDK는 명시적인 기능 계약만 외부에 노출한다.
2. 다른 모듈의 내부 Python 클래스를 직접 import하지 않는다.
3. 등록·활성화·검증·실행·중단·제거 수명주기를 분리한다.
4. 모듈 권한은 매니페스트 요청을 믿지 않고 Policy Gate와 OS 권한으로 집행한다.
5. 플러그인 실패는 기본 검색 코어의 기능을 망가뜨리면 안 된다.
6. LoRA 자동 합성은 기본으로 하지 않는다.
7. 모듈별 설치 크기·로드 시간·Peak RAM/VRAM을 평가한다.
8. 외부 플러그인의 서명 검증·샌드박스 실행이 없으면 실행 허용 대상이 아니다.

## 4. 계약 발전 방식

- 호환성이 깨지는 변경은 별도 `schema_version`으로 관리한다.
- 변환기와 회귀 테스트 없이 기존 매니페스트의 의미를 바꾸지 않는다.
- 기본으로 활성화된 모듈이 없어도 앱 설치와 검색 UI가 정상 동작해야 한다.
- P0는 내부 Module Registry와 안전한 실행 계약. 외부 모듈 SDK 배포는 P2.

## 5. 미구현

- 동적 모듈 로더, 서명, 플러그인 sandbox, 자동 업데이트, 실시간 LoRA 교체, 모델 특화 라우터.
- `entrypoint: NOT_IMPLEMENTED`는 예시 문자열이며 실행 코드가 아니다.
