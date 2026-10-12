# iOS 접근성

iOS가 대상일 때 읽는다. VoiceOver, Switch Control, Voice Control, AssistiveTouch와 Dynamic Type·굵은 글자·모션 감소·투명도 감소를 확인한다.

## 검사

| 영역 | 확인 | 기준 |
| --- | --- | --- |
| 의미 정보 | 적절한 제목과 VoiceOver 탐색 | 2.4.6 AA |
| Cupertino | 레이블·역할·값·상태, 중복 래퍼 방지 | 4.1.2 A |
| 비동기 | 상태 메시지가 실제로 읽힘 | 4.1.3 AA |
| 조작 | Switch Control이 모든 기능에 도달 | 2.1.1 A |
| 텍스트 | 200%와 기기의 큰 접근성 크기, 약 3배 시뮬레이션 | 1.4.4 AA 및 플랫폼 검사 |
| 모션 | Reduce Motion 반영 | 2.3.3 AAA 또는 권장 검사 |
| 대비 | 투명도 감소 상태에서도 읽힘 | 1.4.11 AA |
| 포커스 | 키보드·하단 안전 영역에 가리지 않음 | 2.4.11 AA |

## 검증

Xcode Accessibility Inspector와 실제 기기의 VoiceOver·키보드를 사용한다. `iOSTapTargetGuideline`은 44pt 기준이며 WCAG의 CSS px와 구분한다.

## Flutter 확인 사항

live region만으로 전달되지 않는 문제가 재현될 때 대상 SDK의 announcement API를 검토한다. 오래된 API 예제는 SDK 문서와 대조하고, 잦은 알림과 사용자 발화 방해를 피한다.

```dart
Semantics(
  liveRegion: true,
  child: Text('Status: $status'),
)
SemanticsService.announce('Status changed to $status', TextDirection.ltr);
```

상호작용 중 알림이 끊기는지, 제목 계층이 실제로 어떻게 노출되는지 확인한다. 고대비·반전 플래그는 플랫폼 지원을 확인한다.

```dart
final features = MediaQuery.of(context).accessibilityFeatures;
if (features.highContrast) {
  // 고대비 색상 적용
}
if (features.invertColors) {
  // 색 반전 처리
}
```

Full Keyboard Access와 외부 키보드, Voice Control의 번호·레이블은 실제 버전에서 테스트한다. 과거의 회귀를 영구적인 제약으로 단정하지 않는다.

[Apple 접근성](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Flutter 접근성](https://docs.flutter.dev/ui/accessibility)을 참고한다.
