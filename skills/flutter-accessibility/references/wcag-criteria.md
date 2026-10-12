# WCAG 2.2 주요 기준

이 표는 Flutter 코드 검토에 자주 쓰는 항목이며 WCAG 전체 목록이나 적합성 인증을 대체하지 않는다. AA는 A를, AAA는 A·AA를 포함한다. 기준의 예외·정의는 [WCAG 원문](https://www.w3.org/TR/WCAG22/)에서 확인한다. 2.2에서는 4.1.1 Parsing이 제거되었다.

## A

| ID | 도입 | 기준 | 확인 |
| --- | --- | --- | --- |
| 1.1.1 | 2.0 | Non-text Content | 정보성 이미지 대체 텍스트, 장식 제외 |
| 1.3.1 | 2.0 | Info and Relationships | 역할과 레이블·값 관계, 올바른 의미 병합 |
| 1.3.2 | 2.0 | Meaningful Sequence | 의미 있는 읽기 순서 |
| 1.3.3 | 2.0 | Sensory Characteristics | 모양·위치·소리만으로 지시하지 않음 |
| 1.4.1 | 2.0 | Use of Color | 색 이외 정보 제공 |
| 2.1.1 | 2.0 | Keyboard | 키보드 조작과 기준의 예외 확인 |
| 2.1.2 | 2.0 | No Keyboard Trap | 포커스 탈출 가능 |
| 2.3.1 | 2.0 | Three Flashes or Below Threshold | 초당 3회 이하 또는 일반·적색 섬광 임계값 이하 |
| 2.4.1 | 2.0 | Bypass Blocks | 반복 영역 건너뛰기 |
| 2.4.2 | 2.0 | Page Titled | 웹 페이지의 설명적 제목 |
| 2.4.3 | 2.0 | Focus Order | 의미를 유지하는 순서 |
| 2.5.3 | 2.1 | Label in Name | 접근성 이름에 보이는 레이블 포함 |
| 3.2.6 | 2.2 | Consistent Help | 도움말의 일관된 상대 순서 |
| 3.3.1 | 2.0 | Error Identification | 오류를 텍스트로 알림 |
| 3.3.2 | 2.0 | Labels or Instructions | 입력 레이블·설명 |
| 3.3.7 | 2.2 | Redundant Entry | 동일 과정의 재입력 최소화, 예외 확인 |
| 4.1.2 | 2.0 | Name, Role, Value | 이름·역할·값·상태 |

## AA 추가

| ID | 도입 | 기준 | 확인 |
| --- | --- | --- | --- |
| 1.3.4 | 2.1 | Orientation | 본질적 이유 없는 방향 고정 피함 |
| 1.3.5 | 2.1 | Identify Input Purpose | 해당 개인정보의 autofillHints |
| 1.4.3 | 2.0 | Contrast (Minimum) | 일반 글자 4.5:1, 큰 글자 3:1, 예외 확인 |
| 1.4.4 | 2.0 | Resize Text | 200% 확대에서 내용·기능 유지 |
| 1.4.5 | 2.0 | Images of Text | 텍스트 이미지 대신 실제 글자 |
| 1.4.10 | 2.1 | Reflow | 320 CSS px 상당 폭, 예외 확인 |
| 1.4.11 | 2.1 | Non-text Contrast | 필요한 UI·시각 정보 3:1 |
| 1.4.12 | 2.1 | Text Spacing | 간격 변경에도 손실 없음 |
| 1.4.13 | 2.1 | Content on Hover or Focus | 닫기·포인터 이동·유지 가능 |
| 2.4.5 | 2.0 | Multiple Ways | 페이지를 찾는 여러 방법 |
| 2.4.6 | 2.0 | Headings and Labels | 설명적 제목·레이블 |
| 2.4.7 | 2.0 | Focus Visible | 키보드 포커스 표시 |
| 2.4.11 | 2.2 | Focus Not Obscured (Minimum) | 작성자 콘텐츠에 완전히 가리지 않음 |
| 2.5.7 | 2.2 | Dragging Movements | 드래그 없는 단일 포인터 대안 |
| 2.5.8 | 2.2 | Target Size (Minimum) | 24×24 CSS px 또는 기준의 간격·동등 대안 등 예외 |
| 3.1.2 | 2.0 | Language of Parts | 언어가 바뀌는 부분 표시 |
| 3.2.3 | 2.0 | Consistent Navigation | 일관된 이동 구조 |
| 3.2.4 | 2.0 | Consistent Identification | 같은 기능의 일관된 식별 |
| 3.3.3 | 2.0 | Error Suggestion | 가능한 오류 교정 안내 |
| 3.3.4 | 2.0 | Error Prevention (Legal, Financial, Data) | 되돌림·검사·확인 |
| 3.3.8 | 2.2 | Accessible Authentication (Minimum) | 인지 테스트 제한과 허용 예외·보조 방법 확인 |
| 4.1.3 | 2.1 | Status Messages | 포커스 이동 없이 상태 메시지 인식 가능 |

## AAA 추가

| ID | 도입 | 기준 | 확인 |
| --- | --- | --- | --- |
| 1.4.6 | 2.0 | Contrast (Enhanced) | 일반 7:1, 큰 글자 4.5:1 |
| 2.1.3 | 2.0 | Keyboard (No Exception) | 모든 기능 키보드 접근 |
| 2.2.3 | 2.0 | No Timing | 필수 예외 외 시간 제한 없음 |
| 2.2.6 | 2.1 | Timeouts | 비활성으로 인한 데이터 손실 경고 |
| 2.3.2 | 2.0 | Three Flashes | 어느 1초 동안에도 3회 초과 섬광 없음 |
| 2.3.3 | 2.1 | Animation from Interactions | 본질적이지 않은 상호작용 모션 끄기 |
| 2.4.8 | 2.0 | Location | 현재 위치 정보 |
| 2.4.9 | 2.0 | Link Purpose (Link Only) | 링크 자체로 목적 파악 |
| 2.4.12 | 2.2 | Focus Not Obscured (Enhanced) | 포커스 요소의 일부도 가리지 않음 |
| 2.4.13 | 2.2 | Focus Appearance | 최소 2 CSS px 둘레 상당 면적, 상태 간 3:1 등 조건 |
| 2.5.5 | 2.1 | Target Size (Enhanced) | 44×44 CSS px, 예외 확인 |
| 2.5.6 | 2.1 | Concurrent Input Mechanisms | 입력 방식 불필요한 제한 없음 |
| 3.2.5 | 2.0 | Change on Request | 요청에 의한 문맥 변경 |
| 3.3.5 | 2.0 | Help | 문맥에 맞는 도움말 |
| 3.3.6 | 2.0 | Error Prevention (All) | 모든 제출의 오류 방지 |
| 3.3.9 | 2.2 | Accessible Authentication (Enhanced) | 인지 테스트 없이 인증하거나 대안·보조 메커니즘 제공 |

iOS의 큰 접근성 글자 크기 등 플랫폼 확장 검증은 별도 권장 검사다. WCAG의 CSS px와 네이티브 논리 픽셀·pt를 무조건 같다고 가정하지 않는다.
