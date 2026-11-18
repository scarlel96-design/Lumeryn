# Lumeryn 모델 레지스트리·정책 규칙 초기 계약

> 모델 가중치나 정책 엔진이 구현된 상태가 아니다. JSON Schema 및 예시는 검증용 메타데이터다.

## 모델 매니페스트

`schemas/model-manifest.schema.json`을 사용한다.

- `role=PROPOSED`: 미다운로드·미검증 모델 후보. revision/hash가 null일 수 있다.
- `role=ORIGINAL`: 다운받은 원본의 정확한 revision, 해시 기록.
- `role=DEV`: 실험용 모델/어댑터.
- `role=STABLE`: 실제 평가 후 승격. 검증된 weights hash, revision, benchmark 필수.

원본·Dev·Stable은 별도 보관한다. 같은 모델 ID로 임의 덮어쓰기를 금지한다.
주력 모델, Tokenizer, Vision Processor, Projector, 양자화, 런타임의 호환성을 별도 실험으로 검증한다.
모델 파일은 Git에 넣지 않는다. 예시 매니페스트에는 해시를 발명하지 않고 null로 둔다.

예시: `configs/models/qwen35-4b-proposed.json`.

## 정책 규칙

`schemas/policy-rule.schema.json`을 사용한다.

- 응답 정책, 검색 정책, 도구 권한, 모델 및 모듈 규칙을 구분한다.
- `scope`, `priority`, `conditions`, `decision`을 버전별로 저장한다.
- `ALLOW / ALLOW_WITH_CONDITIONS / REVIEW / REQUIRE_APPROVAL / DENY`를 지원하도록 설계한다.
- 명시적 정책 충돌은 자동 허용하지 않는다.
- 실제 도구 실행은 Policy Gate 및 OS 권한으로 강제한다.
- 안전·윤리·거부 기준 편집과 모델의 학습된 행동 성향은 별개로 취급한다.

예시 `configs/policies/example-search-review.json`은 `enabled=false`다.
정책 실행·충돌 탐지·OPA 연동은 아직 구현되지 않았다.

## 정적 검사

```powershell
py -3.12 -m pip install -e ".[dev]"
py -3.12 scripts/validate_contracts.py model configs/models/qwen35-4b-proposed.json
py -3.12 scripts/validate_contracts.py policy configs/policies/example-search-review.json
```

스키마 적합성은 모델/정책의 안전성, 추론 성능, 실제 엔진 실행 가능성을 보증하지 않는다.
