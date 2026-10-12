# Android 접근성

Android가 대상일 때만 읽는다. TalkBack, Switch Access, Voice Access와 시스템 글자 크기·굵기·색 반전·모션 설정을 확인한다. 설정 경로와 지원 범위는 OS·제조사별로 다를 수 있다.

## 검사

| 영역 | 확인 | 기준 |
| --- | --- | --- |
| 의미 정보 | Stack의 읽기 순서, 정적 레이블 병합과 sortKey | 1.3.2 A |
| 조작 | 길게 누르기 전용 기능의 접근 가능한 대안 | 4.1.2 A |
| 키보드·스위치 | 모든 기능 접근과 포커스 순서 | 2.1.1 A |
| 글자 | 200% 및 실제 기기의 큰 글자에서 잘림 없음 | 1.4.4 AA |
| 색 | 반전·상태 표시가 의미를 잃지 않음 | 1.4.1 A |
| 모션 | disableAnimations 대응 | 2.3.3 AAA 또는 권장 검사 |
| 포커스 | 헤더·스낵바·키보드에 완전히 가리지 않음 | 2.4.11 AA |

## 검증 도구

Accessibility Scanner와 실제 TalkBack·Switch Access를 사용한다. `androidTapTargetGuideline`의 48dp는 Android 권장 검사이며 WCAG AA의 24 CSS px와 구분한다. 테스트에서는 `ensureSemantics`, `getSemantics`, `matchesSemantics`를 사용한다.

## Flutter 확인 사항

- 제목 여부와 제목 수준의 플랫폼 매핑을 구분한다. `header`·`headingLevel`의 실제 읽기를 대상 Flutter 버전에서 확인한다.
- `liveRegion`의 실제 알림을 확인하고 중복 announcement를 피한다.
- `identifier`는 UI 테스트 식별용이며 사용자 레이블을 대신하지 않는다.

```dart
Semantics(
  identifier: 'submit-button',
  child: ElevatedButton(...),
)
```

글자 굵기 플래그 등은 대상 OS에서 지원되는지 확인한다.

```dart
if (MediaQuery.of(context).accessibilityFeatures.boldText) {
  // 굵은 글자 적용
}
```

앱 시작 시점과 설정 변경 직후의 모션 플래그를 모두 테스트한다. 특정 Flutter 버전의 회귀 이슈를 모든 버전의 사실로 일반화하지 않는다. 길게 누르기만 있는 InkWell은 TalkBack의 기본 활성화 동작으로 기능에 접근할 수 있는지 확인한다.

[Android 접근성](https://developer.android.com/guide/topics/ui/accessibility), [Flutter 접근성](https://docs.flutter.dev/ui/accessibility)을 참고한다.
