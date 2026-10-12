# Windows 접근성

Windows가 대상일 때 읽는다. Narrator, NVDA, JAWS와 키보드·고대비 테마를 확인한다. OS 설정과 단축키는 버전에 맞춰 사용한다.

## 검사

| 영역 | 확인 | 기준 |
| --- | --- | --- |
| 의미 정보 | 이미지·아이콘 레이블, 폼 레이블과 상태 | 1.1.1·3.3.2·4.1.2 A |
| 탐색 | 실제 화면 낭독의 탐색 모드와 제목 접근 | 1.3.2 A·2.4.6 AA |
| 대비 | 고대비에서 색상 역할과 시각 정보 | 1.4.11 AA |
| 포커스 | 표시·가림 없음 | 2.4.7·2.4.11 AA |
| 강화 표시 | 면적·대비 기준 | 2.4.13 AAA |
| 키보드 | Tab·Shift+Tab·Enter·Space·화살표와 표준 단축키 | 2.1.1 A |
| 대상 | 크기·간격·예외와 배율 | 2.5.8 AA |

## 검증

Narrator·NVDA·JAWS 중 지원 조합과 Windows SDK Inspect로 UI Automation 트리를 확인한다. 키보드 전용 흐름도 수행한다.

## Flutter 확인 사항

시스템 색상 사용 예제는 설치 Flutter 버전과 실제 Windows 고대비 지원을 확인해 적용한다. 플래그나 테마 옵션 하나로 고대비 준수를 보장하지 않는다.

```dart
ThemeData(
  useMaterial3: true,
  useSystemColors: true, // 실제 Windows 고대비 반영 여부는 대상 SDK·OS에서 확인한다.
)
```

브라우저의 NVDA 탐색 모드와 네이티브 앱 동작을 동일하게 가정하지 않는다. SemanticsRole·제목·UIA 매핑도 대상 버전에서 확인하고 재현된 제한을 기록한다.

[Windows 접근성](https://support.microsoft.com/en-us/accessibility), [UI Automation](https://learn.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32), [Inspect](https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects)를 참고한다.
