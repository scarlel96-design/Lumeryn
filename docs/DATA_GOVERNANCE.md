# Lumeryn 데이터 거버넌스 및 모델 평가 데이터 정책

> 상태: 설계 기준. 실제 수집·학습은 아직 시작하지 않았다.

## 1. 저장 영역 분리

| 영역 | 데이터 | 관리 |
|---|---|---|
| Local User Store | 대화, 설정, 선택한 개인 자료 | 사용자 삭제·내보내기 |
| Web Evidence Store | 검색 원문, URL, 해시, 수집 시각 | 출처·기한·재수집 |
| Training Candidate | 승인 전 도구 흔적·예제 | 격리·자동/수동 검토 |
| Approved Training | 라이선스·품질·출처 검증된 사례 | 버전·중복 제거 |
| Evaluation | 개발·검증·블라인드 정답 | 학습 데이터와 독립 |
| Model Artifacts | 원본 모델, LoRA, Processor 등 | immutable 해시·승격 |

대화 데이터를 자동으로 학습 데이터로 사용하지 않는다. 사용자 승인과 데이터 출처 검증을 요구한다.

## 2. 문서·이미지 근거 필드

`source_id`, `canonical_url`, `published_at`(모르면 null), `retrieved_at`, `sha256`, `document_version`, `license_status`, `source_type`, `page/region`, `verification_status`를 관리한다.

날짜가 확인되지 않은 정보를 최신 정보로 단정하지 않는다.
이미지 분석 결과는 픽셀 관측과 외부 사실 검증 상태를 구분한다.

## 3. 데이터셋 승인 파이프라인

수집 → 후보 격리 → 중복/품질/PII/라이선스 검사 → 원문/정답 검증 → 승인 → 버전 고정 → 학습 → 블라인드 평가.

- 모델이 자동 생성한 정답은 검증 전까지 **후보**로만 저장한다.
- 동일 문서나 사건에서 파생한 사례가 학습/최종 블라인드 평가를 함께 오염시키지 않도록 그룹 단위로 분리한다.
- 최신 정보 데이터는 평가 시점과 외부 검색 환경을 기록한다.
- 데이터셋 출처 URL이 사라지더라도 검증·저장 가능 여부를 확인한다.

## 4. 라이선스 및 삭제

수집, 로컬 분석, 모델 학습, 재배포는 서로 다른 권한이다. 이용약관과 자료 라이선스를 각 단계에서 확인한다.
사용자 자료 삭제는 대화 기록, 캐시, 임베딩 및 관련 개인 파일 인덱스까지 적용되도록 설계한다.
복구 백업과 학습 완료된 가중치에 대한 삭제 정책은 별도의 릴리스 전 결정이 필요하다.

## 5. 평가

최소 세 군:
1. 원본 Qwen3.5-4B (도구 없음).
2. 원본 모델 + Lumeryn 검색 코어.
3. 튜닝 모델 + 동일 검색 코어.

같은 문항·시간대·출처 접근 정책·검색 예산·하드웨어 조건을 기록한다.
평가를 통과하지 않은 어댑터는 Stable에 승격하지 않는다.
500문항과 14,000개 데이터 목표는 **제안된 규모**이며 실측 완료값이 아니다.

## 6. 감사 항목

- 학습 데이터 manifest의 SHA-256
- 원본 모델 revision, adapter revision, tokenizer/processor 정보
- 학습 recipe·seed·환경 lockfile
- 학습/검증/블라인드 분할
- 사용자 동의 범위
- 평가 결과와 회귀·퇴화 분석

## 참고

- Hugging Face model card: https://huggingface.co/Qwen/Qwen3.5-4B
- Python Packaging Guide: https://packaging.python.org/en/latest/
