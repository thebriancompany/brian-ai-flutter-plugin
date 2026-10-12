---
name: flutter-accessibility
description: "Flutter 위젯의 접근성을 감사하거나 개선할 때 사용한다. WCAG 목표 수준과 플랫폼별 의미 정보, 키보드, 대비, 확대, 모션과 폼을 검증한다."
---

# Flutter 접근성

WCAG 2.2의 목표 수준과 대상 플랫폼에 맞춰 위젯을 검토·개선한다. 현재 단계에 필요한 참고 문서만 읽는다.

## 범위 확인

요청과 프로젝트 문서에서 목표 수준(A, AA, AA와 선택한 AAA, AAA)과 대상 플랫폼(iOS, Android, Web, macOS, Windows, Linux)을 확인한다. 감사 범위를 결정할 정보가 없으면 Codex의 질문 도구 또는 짧은 일반 질문으로 필요한 항목을 한 번에 묻는다. 이미 정해진 목표는 다시 묻지 않는다. 단일 위젯의 명확한 수정 요청은 그 범위에서 진행한다.

AA는 A를 포함하고 AAA는 A·AA를 포함한다. 선택한 AAA 항목은 ID로 기록한다. 기준 적용 여부와 실제 영향도를 분리한다.

## 핵심 기준

- 정보성 이미지는 `semanticLabel`·`Semantics(label:)`, 장식 이미지는 `excludeFromSemantics: true`로 구분한다.
- 단독 `GestureDetector`로 버튼을 만들면 키보드 동작이 빠질 수 있다. Material 버튼 또는 포커스·키보드·의미 체계를 갖춘 구현을 쓴다.
- WCAG AA 목표 크기는 24×24 CSS px 기준과 예외를 확인한다. AAA는 44×44 CSS px 기준을 확인한다. 모바일의 48dp 권장은 별도 플랫폼 권장사항으로 표시하며 AA 위반과 혼동하지 않는다.
- 드래그에는 같은 기능의 단일 포인터 대안을 제공한다. 삭제 버튼·위아래 이동 버튼 등이며 키보드 대안만으로 2.5.7을 충족한다고 단정하지 않는다.
- 포커스된 요소가 헤더·하단바·키보드 등에 가리지 않는지 확인한다. 필요하면 `Scrollable.ensureVisible`과 인셋 대응을 사용한다.
- 색만으로 상태를 전달하지 않는다. 문구·아이콘·형태를 함께 쓴다.
- 시스템의 모션 감소 설정을 존중한다. 컨트롤러·암시적 위젯·Hero·라우트 전환을 확인한다. AAA 기준과 일반 권장사항을 구분한다.
- 아이콘 전용 버튼에는 목적을 알 수 있는 tooltip·의미 레이블을 제공한다.
- 의미 있는 내용이나 버튼을 `ExcludeSemantics`로 숨기지 않는다. 정적인 레이블·값만 `MergeSemantics`로 묶고 독립 조작 요소는 분리한다.
- 고정 높이로 큰 텍스트가 잘리지 않게 최소 높이·유연한 배치를 사용한다.
- 대비는 목표 수준에 맞춰 측정한다. Cupertino 위젯도 실제 의미 트리를 확인하고 누락된 레이블·값·상태만 보완한다.
- 개인정보 입력 필드에 적절한 `autofillHints`·레이블을 제공한다. 복사·붙여넣기·비밀번호 관리자를 막지 않는다.
- 비동기 상태 메시지는 live region 등으로 전달하되 플랫폼별 실제 읽기와 중복·과도한 알림을 확인한다.

## 감사 절차

선택한 플랫폼 파일과 [WCAG 표](references/wcag-criteria.md)를 읽고 다음을 확인한다.

1. 의미 정보·화면 낭독·읽기 순서
2. 조작 대상 크기·드래그 대안
3. 포커스·키보드·대화상자·가림
4. 텍스트·컴포넌트 대비
5. 텍스트 확대·줄바꿈·작은 화면
6. 모션 감소·깜박임
7. 폼·인증·도움말

화면을 실행해야 판별할 내용은 미검증 항목으로 기록한다. 코드에서 근거를 찾지 못한 것을 확정 결함으로 보고하지 않는다.

## 결과 형식

각 발견에는 위치, 플랫폼, 기준 ID와 이름·수준, `CRITICAL`·`MAJOR`·`MINOR` 중 영향도, 문제, 수정 전후 Dart 코드를 포함한다. 예:

- 위치: `lib/cart/view/summary.dart:42`
- 기준: `2.5.8 Target Size (Minimum), AA, WCAG 2.2`
- 영향: `MAJOR` — 실제 작은 포인터 대상 때문에 조작이 어려움

수정 전:

```dart
SizedBox(
  width: 16,
  height: 16,
  child: GestureDetector(onTap: onClose, child: const Icon(Icons.close)),
)
```

수정 후:

```dart
IconButton(
  onPressed: onClose,
  tooltip: context.l10n.closeOrderSummary,
  constraints: const BoxConstraints(minWidth: 48, minHeight: 48),
  icon: const Icon(Icons.close),
)
```

[보고서 템플릿](references/audit-templates.md)에 검사 범위·확인한 통과 항목·미검증 사항을 정리한다. 플랫폼별 영향이 다르면 구분한다.

## 수정과 검증

감사만 요청했다면 보고서를 제공하고, 수정을 이미 요청했다면 승인된 범위의 수정을 바로 수행한다. 추가 범위 선택이 필요할 때만 묻는다. [테스트](references/testing.md)로 회귀를 검증하고, 실제 화면 낭독이 필요한 경우 실행 여부를 분명히 기록한다.

## 자주 발견되는 패턴

의미 정보:

```dart
// 잘못된 예: 빈 레이블·누락된 레이블·조작 요소 위 ExcludeSemantics
// 버튼이 의미 트리에서 제거되어 화면 낭독 사용자가 조작할 수 없다.
Image.asset('assets/warning.png', semanticLabel: '')
Image.asset('assets/chart.png')
ExcludeSemantics(child: ElevatedButton(onPressed: _submit, child: const Text('Submit')))
```

```dart
// 확인 필요: 의미 정보가 부족한 Cupertino 위젯
CupertinoSwitch(value: _enabled, onChanged: _onChanged)
```

```dart
// 잘못된 예: 조작 가능한 자식을 병합해 버튼 역할이 사라짐
MergeSemantics(
  child: Row(children: [const Text('Item'), IconButton(onPressed: _delete, icon: ...)]),
)
```

대상 크기·드래그:

```dart
// 확인 필요: 16×16 대상의 WCAG 2.5.8 크기·간격·예외
SizedBox(width: 16, height: 16, child: GestureDetector(onTap: _onTap, child: const Icon(Icons.close, size: 16)))
```

```dart
// 잘못된 예: 드래그 없는 대안이 없는 Dismissible, WCAG 2.5.7
Dismissible(key: ValueKey(item.id), onDismissed: (_) => _delete(item), child: ListTile(title: Text(item.name)))
```

포커스:

```dart
// 잘못된 예: 키보드 동작을 제공하지 않은 GestureDetector
GestureDetector(onTap: _onTap, child: const Text('Click me'))
```

```dart
// 잘못된 예: 하단 바가 포커스된 TextField를 가림, WCAG 2.4.11
Scaffold(
  resizeToAvoidBottomInset: false,
  bottomNavigationBar: const BottomAppBar(child: ...),
  body: ListView(children: [..., TextField(focusNode: _last), ...]),
)
```

글자 확대·모션:

```dart
// 잘못된 예: 글자 확대 시 텍스트가 잘림
SizedBox(height: 48, child: Text('Status: Ready'))
```

```dart
// 잘못된 예: 모션 감소 설정과 무관하게 항상 재생
AnimatedContainer(duration: const Duration(milliseconds: 500), color: ..., child: child)
```

## 참고 문서

- [기준](references/wcag-criteria.md), [보고서](references/audit-templates.md)
- [수정 예제](references/examples.md), [위젯별 요구](references/widget-mapping.md), [테스트](references/testing.md)
- [iOS](references/platforms/ios.md), [Android](references/platforms/android.md), [Web](references/platforms/web.md)
- [macOS](references/platforms/macos.md), [Windows](references/platforms/windows.md), [Linux](references/platforms/linux.md)
- [WCAG 원문](https://www.w3.org/TR/WCAG22/), [기준 해설](https://www.w3.org/WAI/WCAG22/Understanding/), [Flutter 접근성](https://docs.flutter.dev/ui/accessibility)
