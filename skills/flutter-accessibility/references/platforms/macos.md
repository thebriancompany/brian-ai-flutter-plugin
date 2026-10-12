# macOS 접근성

macOS가 대상일 때 읽는다. VoiceOver, 전체 키보드 접근, 모션 감소와 대비 증가 설정을 확인한다.

## 검사

| 영역 | 확인 | 기준 |
| --- | --- | --- |
| 포커스 | 키보드 설정과 무관하게 명확한 표시 | 2.4.7 AA |
| 대화상자 | 포커스 진입·순환·복원과 표시 | 2.4.7 AA·2.4.13 AAA |
| 가림 | 고정 바·오버레이에 완전히 가리지 않음 | 2.4.11 AA |
| 대비 | 실제 OS 고대비 설정에서 읽힘 | 1.4.11 AA |
| 모션 | 감소 설정 반영 | 2.3.3 AAA 또는 권장 검사 |
| 의미 정보 | VoiceOver 키보드 탐색과 이미지 레이블 | 1.3.2·1.1.1 A |
| 키보드 | 기능별 표준 단축키와 모든 조작 | 2.1.1 A |

## 검증

Xcode Accessibility Inspector와 실제 VoiceOver 명령을 사용한다. 모바일 스와이프만으로 검증했다고 간주하지 않는다. 포커스 표시는 실제 위젯 상태와 의미 디버거로 확인한다.

## Flutter 확인 사항

고대비 플래그와 `highContrastTheme`가 실제 OS 설정과 연결되는지 검증한다. MediaQuery만 읽는 것으로 엔진이 제공하지 않는 플래그를 생성할 수는 없다.

```dart
final isHighContrast = MediaQuery.of(context).highContrast;
if (isHighContrast) {
  // 고대비 테마 적용
}
```

`SemanticsRole`·제목 수준의 지원은 현재 SDK와 macOS에서 확인한다. 과거에 웹 전용이었던 동작을 최신 플랫폼 전체에 일반화하지 않는다.

[Apple 접근성](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Flutter macOS](https://docs.flutter.dev/platform-integration/macos)를 참고한다.
