# Linux 접근성

Linux가 대상일 때 읽는다. Orca·Speech Dispatcher와 실제 배포판의 GTK·보조 기술 연결을 확인한다.

## 검사

| 영역 | 확인 | 기준 |
| --- | --- | --- |
| 의미 정보 | 이미지·아이콘·폼의 설명적 레이블 | 1.1.1·3.3.2·4.1.2 A |
| 읽기 | 반복하거나 지나치게 긴 레이블 없음 | 4.1.2 A |
| 포커스 | 키보드 표시와 가림 없음 | 2.4.7·2.4.11 AA |
| 키보드 | Tab·Shift+Tab·Enter·Space·화살표, 적절한 단축키 | 2.1.1 A |
| 대상 | WCAG 크기·간격·예외와 플랫폼 배율 | 2.5.8 AA |

## 검증

Orca와 키보드 전용 조작을 실제 배포판에서 테스트한다. 공통 Flutter 의미 테스트도 수행하되 데스크톱 통합 검증을 대체하지 않는다.

## Flutter 확인 사항

복잡한 드롭다운·의미 트리·제목 탐색의 지원은 GTK·Orca·Flutter 조합에서 확인한다. `SemanticsRole`이나 고대비·굵기 플래그의 다른 플랫폼 동작을 그대로 가정하지 않는다. 재현된 제한만 기록한다.

장황한 레이블 예:

```dart
Semantics(
  label: 'Delete item button. Item name is: Item one. Press Space to activate',
  child: IconButton(...)
)
```

간결한 레이블 예:

```dart
IconButton(
  tooltip: 'Delete item',
  onPressed: _delete,
  icon: const Icon(Icons.delete),
)
```

포커스 탐색으로 기능에 접근할 수 있는지 확인하고, 정적 내용까지 무조건 Tab 정지점으로 만들지는 않는다.

[Orca 문서](https://help.gnome.org/users/orca/stable/), [Flutter Linux](https://docs.flutter.dev/platform-integration/linux)를 참고한다.
