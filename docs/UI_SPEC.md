# Lumeryn Windows/UI 디자인 및 검증 규격

> 상태: 디자인 및 테스트 요구사항. 실제 PySide6/QML UI는 아직 미구현.

## Windows 네이티브 프레임 (P0)

- 닫기·최대화/복원·최소화는 Windows 11 원래 창 동작을 유지한다.
- Snap Layouts 호버 및 `Win+Z`, 작업표시줄과 창 그림자, 키보드 이동·화면 간 이동을 시험한다.
- 커스텀 프레임을 초기값으로 선택하지 않는다. Win32 호출과 Qt 상호운용성을 검증한 경우만 승인한다.
- 표준 창 컨트롤을 화면의 디자인 목표 때문에 흉내 내지 않는다.

## 내부 Apple HIG 지향 경험 (P0)

- 공통 디자인 토큰: Colors, Spacing, Radius, Typography, Elevation, Materials, Motion, Iconography, Focus, Accessibility.
- Sidebar, Search Composer, Floating Inspector, Module List, Dialog, Toast, Progress 및 Research Timeline을 재사용 컴포넌트로 만든다.
- UI와 Domain을 직접 결합하지 않는다. ViewModel과 Application DTO를 사용한다.
- Apple 상표·폰트·아이콘 파일을 무단 배포하지 않는다.

## Motion 품질 (P0)

- Spring/SmoothedAnimation, 연결형 화면 전환, 선택/호버 상태의 마이크로 인터랙션.
- Reduce Motion이 활성화되면 불필요한 이동/스케일 대신 낮은 모션 대체 수단을 사용한다.
- 애니메이션은 독립적으로 취소·중단 가능해야 한다.
- 기본 목표 60FPS는 설계값이며 실제 GPU·DPI·창 크기에서 측정한다.
- 텍스트 판독, 포커스, 스크린리더 사용성을 시각 효과보다 우선한다.
- 검색·이미지 처리·모델 추론은 UI 스레드를 막지 않는다.

## 계측 및 수락

| 항목 | 시험 |
|---|---|
| Win11 창 컨트롤 | 실제 OS에서 클릭·호버·단축키·Snap |
| DPI | 100/125/150/200%, 멀티 모니터 |
| 모션 | 60Hz 이상 패널, 저사양 GPU, Reduce Motion |
| 접근성 | 키보드 전체 탐색, 포커스, 명도 대비, Narrator |
| 종료·취소 | 검색 중 창 변경, 백그라운드·재시작 |
| 성능 | 프레임 시간 p50/p95, 메모리, UI 입력 지연 |

CI의 Windows runner는 사용자 PC의 실제 디스플레이 프레임/Win11 Narrator 시험을 대체하지 않는다.

## 작업 연계

`WO-UI-01` 네이티브 창 → `WO-UI-02` 디자인 토큰/컴포넌트 → `WO-UI-03` 모션/접근성 → `WO-19` 통합.

참고: https://developer.apple.com/design/human-interface-guidelines/ 및 https://learn.microsoft.com/windows/apps/develop/title-bar
