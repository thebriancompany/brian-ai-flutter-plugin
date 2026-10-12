# 접근성 개선 예제

앱과 Flutter 버전에 맞춰 적용하는 예제다. 의미 트리를 먼저 확인해 레이블 중복이나 잘못된 역할을 추가하지 않는다. 시연용 문자열은 실제 앱의 지역화로 바꾼다.

## 복합 위젯의 의미 정보

```dart
import 'package:flutter/material.dart';

/// 개별 별 아이콘 대신 하나의 의미 설명을 제공하는
/// 평점 표시 위젯이다.
class const AccessibleRatingBar({
  required final int rating,
  required final int maxRating,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Rating: $rating out of $maxRating stars',
      child: ExcludeSemantics(
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(maxRating, (index) {
            return Icon(
              index < rating ? Icons.star : Icons.star_border,
              color: Colors.amber,
            );
          }),
        ),
      ),
    );
  }
}
```

## Cupertino 의미 정보 보완

내장 역할·값을 확인하고 누락된 정보만 보완한다. 스위치·슬라이더를 일괄 button 역할로 바꾸지 않는다.

```dart
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class const AccessibleCupertinoSwitch({
  required final String label,
  required final bool value,
  required final ValueChanged<bool> onChanged,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: label,
      toggled: value,
      enabled: true,
      child: ExcludeSemantics(
        child: CupertinoSwitch(value: value, onChanged: onChanged),
      ),
    );
  }
}

class const AccessibleCupertinoSlider({
  required final String label,
  required final double value,
  required final double min,
  required final double max,
  required final ValueChanged<double> onChanged,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: label,
      value: value.toStringAsFixed(0),
      slider: true,
      child: ExcludeSemantics(
        child: CupertinoSlider(
          value: value,
          min: min,
          max: max,
          onChanged: onChanged,
        ),
      ),
    );
  }
}
```

## 조작 가능한 내용을 숨기지 않기

```dart
// 잘못된 예: 조작 요소가 있는 행 전체를 ExcludeSemantics로 감쌈
// 전체 하위 트리가 의미 트리에서 제거되어 버튼이
// TalkBack·VoiceOver에 노출되지 않고 조작할 수 없게 된다.
ExcludeSemantics(
  child: Row(
    children: [
      const Text('Total'),
      const Text('42.00 USD'),
      ElevatedButton(onPressed: _submit, child: const Text('Pay now')),
    ],
  ),
)

// 올바른 예: 정적 레이블·값만 병합하고 버튼은 별도 포커스 유지
Row(
  children: [
    MergeSemantics(
      child: Row(children: [const Text('Total'), const Text('42.00 USD')]),
    ),
    ElevatedButton(onPressed: _submit, child: const Text('Pay now')),
  ],
)
```

## MergeSemantics의 범위

```dart
// 올바른 예: 정적 레이블·값을 하나의 읽기 대상으로 병합
MergeSemantics(
  child: Row(
    children: [Text(label), Text(value)],
  ),
)

// 잘못된 예: 조작 가능한 자식을 병합해 역할을 잃음
MergeSemantics(
  child: Row(
    children: [Text(item.name), IconButton(onPressed: _delete, icon: const Icon(Icons.delete))],
  ),
)

// 올바른 예: 정적 내용만 병합하고 버튼은 독립적으로 유지
Row(
  children: [
    MergeSemantics(child: Row(children: [Text(item.name), Text(item.subtitle)])),
    IconButton(onPressed: _delete, icon: const Icon(Icons.delete), tooltip: 'Delete ${item.name}'),
  ],
)
```

## 비동기 상태 메시지

```dart
import 'package:flutter/material.dart';

enum UploadStatus { idle, uploading, success, error }

class const UploadStatusIndicator({required final UploadStatus status, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final icon = switch (status) {
      UploadStatus.idle => const SizedBox.shrink(),
      UploadStatus.uploading => const SizedBox(
          width: 16,
          height: 16,
          child: CircularProgressIndicator(strokeWidth: 2),
        ),
      UploadStatus.success => const Icon(Icons.check_circle, color: Colors.green),
      UploadStatus.error => const Icon(Icons.error, color: Colors.red),
    };

    final label = switch (status) {
      UploadStatus.idle => '',
      UploadStatus.uploading => 'Uploading...',
      UploadStatus.success => 'Upload complete',
      UploadStatus.error => 'Upload failed',
    };

    return Semantics(
      liveRegion: true,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [icon, const SizedBox(width: 8), Text(label)],
      ),
    );
  }
}
```

일회성 알림은 대상 SDK의 지원 API를 확인하고 사용한다. 오래된 `announce` 예제는 최신 SDK에서 `sendAnnouncement`로 이전이 필요할 수 있다.

```dart
SemanticsService.announce('Item added to cart', TextDirection.ltr);
```

## 작은 아이콘의 조작 영역

```dart
import 'package:flutter/material.dart';

/// 작은 위젯을 최소 48×48 조작 영역으로 감싼다.
/// 48dp는 모바일 권장값이며 WCAG AA 최소 기준·예외와 구분한다.
class const AccessibleTapTarget({
  required final VoidCallback onTap,
  required final String semanticLabel,
  required final Widget child,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticLabel,
      button: true,
      child: InkWell(
        onTap: onTap,
        child: ConstrainedBox(
          constraints: const BoxConstraints(minWidth: 48, minHeight: 48),
          child: Center(child: child),
        ),
      ),
    );
  }
}

// 사용 예
AccessibleTapTarget(
  onTap: _onClose,
  semanticLabel: 'Close dialog',
  child: const Icon(Icons.close, size: 16),
)
```

## 스와이프 삭제의 버튼 대안

```dart
class const AccessibleDismissibleListItem({
  required final Item item,
  required final ValueChanged<Item> onDelete,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Dismissible(
      key: ValueKey(item.id),
      direction: DismissDirection.endToStart,
      background: Container(color: Colors.red.shade400),
      onDismissed: (_) => onDelete(item),
      child: ListTile(
        title: Text(item.name),
        trailing: IconButton(
          icon: const Icon(Icons.delete_outline),
          tooltip: 'Delete ${item.name}',
          onPressed: () => onDelete(item),
        ),
      ),
    );
  }
}
```

## 목록 순서 변경의 위·아래 버튼

```dart
class const AccessibleReorderableList({
  required final List<Item> items,
  required final void Function(int oldIndex, int newIndex) onReorder,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ReorderableListView.builder(
      itemCount: items.length,
      onReorder: onReorder,
      itemBuilder: (context, index) {
        final item = items[index];
        final isFirst = index == 0;
        final isLast = index == items.length - 1;
        return ListTile(
          key: ValueKey(item.id),
          title: Text(item.name),
          trailing: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: const Icon(Icons.arrow_upward),
                tooltip: 'Move up',
                onPressed: isFirst ? null : () => onReorder(index, index - 1),
              ),
              IconButton(
                icon: const Icon(Icons.arrow_downward),
                tooltip: 'Move down',
                // 아래로 이동할 때 ReorderableListView의 onReorder는 index + 1을 사용한다.
                onPressed: isLast ? null : () => onReorder(index, index + 2),
              ),
              const Icon(Icons.drag_handle),
            ],
          ),
        );
      },
    );
  }
}
```

## 슬라이더 키보드·버튼 조작

키보드 지원과 별개로 2.5.7은 단일 포인터 대안도 확인한다.

```dart
class const AccessibleSlider({
  required final String label,
  required final double value,
  required final ValueChanged<double> onChanged,
  final double min = 0,
  final double max = 100,
  final double step = 1,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        IconButton(
          icon: const Icon(Icons.remove),
          tooltip: 'Decrease ${label.toLowerCase()}',
          onPressed: value > min ? () => onChanged((value - step).clamp(min, max)) : null,
        ),
        Expanded(
          child: Semantics(
            label: label,
            value: value.toStringAsFixed(0),
            slider: true,
            child: Slider(value: value, min: min, max: max, onChanged: onChanged),
          ),
        ),
        IconButton(
          icon: const Icon(Icons.add),
          tooltip: 'Increase ${label.toLowerCase()}',
          onPressed: value < max ? () => onChanged((value + step).clamp(min, max)) : null,
        ),
      ],
    );
  }
}
```

## 폼의 포커스 순서

```dart
import 'package:flutter/material.dart';

class AccessibleForm extends StatelessWidget {
  const AccessibleForm({super.key});

  @override
  Widget build(BuildContext context) {
    return FocusTraversalGroup(
      policy: OrderedTraversalPolicy(),
      child: Column(
        children: [
          FocusTraversalOrder(
            order: const NumericFocusOrder(1),
            child: TextFormField(
              decoration: const InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
              autofillHints: const [AutofillHints.email],
              textInputAction: TextInputAction.next,
            ),
          ),
          const SizedBox(height: 16),
          FocusTraversalOrder(
            order: const NumericFocusOrder(2),
            child: TextFormField(
              decoration: const InputDecoration(labelText: 'Password'),
              obscureText: true,
              autofillHints: const [AutofillHints.password],
              textInputAction: TextInputAction.done,
            ),
          ),
          const SizedBox(height: 24),
          FocusTraversalOrder(
            order: const NumericFocusOrder(3),
            child: ElevatedButton(
              onPressed: () {},
              child: const Text('Sign In'),
            ),
          ),
        ],
      ),
    );
  }
}
```

## 고정 헤더와 포커스 가림

```dart
class const FocusEnsureVisibleField({
  required final String label,
  required final double stickyHeaderHeight,
  super.key,
}) extends StatefulWidget {
  @override
  State<FocusEnsureVisibleField> createState() => _FocusEnsureVisibleFieldState();
}

class _FocusEnsureVisibleFieldState extends State<FocusEnsureVisibleField> {
  final _focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(_handleFocus);
  }

  void _handleFocus() {
    if (_focusNode.hasFocus) {
      Scrollable.ensureVisible(
        context,
        alignment: 0.5,
        duration: const Duration(milliseconds: 200),
      );
    }
  }

  @override
  void dispose() {
    _focusNode.removeListener(_handleFocus);
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      // 고정 헤더 아래 공간을 확보해 포커스된 필드가 보이게 한다.
      padding: EdgeInsets.only(top: widget.stickyHeaderHeight + 8),
      child: TextField(
        focusNode: _focusNode,
        decoration: InputDecoration(labelText: widget.label),
      ),
    );
  }
}
```

## AAA 포커스 표시

```dart
class const FocusAppearanceWrap({
  required final VoidCallback onPressed,
  required final Widget child,
  super.key,
}) extends StatefulWidget {
  @override
  State<FocusAppearanceWrap> createState() => _FocusAppearanceWrapState();
}

class _FocusAppearanceWrapState extends State<FocusAppearanceWrap> {
  bool _focused = false;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return FocusableActionDetector(
      onFocusChange: (hasFocus) => setState(() => _focused = hasFocus),
      actions: {
        ActivateIntent: CallbackAction<ActivateIntent>(
          onInvoke: (_) {
            widget.onPressed();
            return null;
          },
        ),
      },
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: widget.onPressed,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 100),
          decoration: BoxDecoration(
            border: Border.all(
              width: _focused ? 2 : 0,
              color: _focused ? scheme.primary : Colors.transparent,
            ),
            borderRadius: BorderRadius.circular(8),
          ),
          child: widget.child,
        ),
      ),
    );
  }
}
```

## 대비를 고려한 테마

실제 색상 조합으로 비율을 측정한다.

```dart
import 'package:flutter/material.dart';

ThemeData buildAccessibleTheme() {
  const colorScheme = ColorScheme(
    brightness: Brightness.light,
    primary: Color(0xFF1565C0),       // 파랑 800
    onPrimary: Color(0xFFFFFFFF),     // 흰색, primary와 8.6:1
    secondary: Color(0xFF00695C),     // 청록 800
    onSecondary: Color(0xFFFFFFFF),   // 흰색, secondary와 7.1:1
    error: Color(0xFFB71C1C),         // 빨강 900
    onError: Color(0xFFFFFFFF),       // 흰색, error와 7.8:1
    surface: Color(0xFFFFFFFF),       // 흰색
    onSurface: Color(0xFF212121),     // 회색 900, 흰색과 16:1
  );

  return ThemeData(
    colorScheme: colorScheme,
    textTheme: const TextTheme(
      bodyLarge: TextStyle(fontSize: 16, height: 1.5),
      bodyMedium: TextStyle(fontSize: 14, height: 1.5),
    ),
  );
}
```

## 색 이외 상태 표시

```dart
class const AccessibleStatusBadge({required final TaskStatus status, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final (icon, label, color) = switch (status) {
      TaskStatus.pending => (Icons.hourglass_empty, 'Pending', Colors.orange),
      TaskStatus.active => (Icons.play_circle, 'Active', Colors.blue),
      TaskStatus.complete => (Icons.check_circle, 'Complete', Colors.green),
      TaskStatus.error => (Icons.error, 'Error', Colors.red),
    };

    // 색만으로 전달하지 않고 아이콘과 레이블을 함께 제공한다.
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(width: 4),
        Text(label),
      ],
    );
  }
}

enum TaskStatus { pending, active, complete, error }
```

## 큰 글자에 적응하는 카드

Android·웹 200%와 iOS의 큰 접근성 크기 등 목표 환경에서 확인한다.

```dart
class const AdaptiveInfoCard({
  required final String title,
  required final String description,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 고정 높이 없이 텍스트가 늘어날 수 있게 한다.
            Text(title, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            // 고정 높이 대신 ConstrainedBox의 minHeight를 사용한다.
            ConstrainedBox(
              constraints: const BoxConstraints(minHeight: 40),
              child: Text(
                description,
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 모션 감소를 존중하는 라우트

```dart
import 'package:flutter/material.dart';

class AccessiblePageRoute<T> extends MaterialPageRoute<T> {
  AccessiblePageRoute({required super.builder, super.settings});

  @override
  Widget buildTransitions(
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget child,
  ) {
    if (MediaQuery.of(context).disableAnimations) {
      return child; // 화면을 즉시 전환한다.
    }
    return super.buildTransitions(context, animation, secondaryAnimation, child);
  }
}
```

## 모션 감소와 Hero

```dart
class const AccessibleHero({required final Object tag, required final Widget child, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    if (MediaQuery.of(context).disableAnimations) {
      return child;
    }
    return Hero(tag: tag, child: child);
  }
}
```

## 중복 입력 방지

```dart
class CheckoutEmailField extends StatelessWidget {
  const CheckoutEmailField({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<CheckoutBloc, CheckoutState>(
      buildWhen: (prev, next) => prev.email != next.email,
      builder: (context, state) {
        return TextField(
          controller: TextEditingController(text: state.email),
          decoration: const InputDecoration(labelText: 'Email'),
          keyboardType: TextInputType.emailAddress,
          autofillHints: const [AutofillHints.email],
          onChanged: (v) => context.read<CheckoutBloc>().add(EmailChanged(v)),
        );
      },
    );
  }
}
```

## 붙여넣기·비밀번호 관리자 지원

```dart
class const AccessiblePasswordField({required final TextEditingController controller, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      obscureText: true,
      // 붙여넣기가 가능해야 하므로 상호작용 선택 기능을 끄지 않는다.
      enableInteractiveSelection: true,
      autofillHints: const [AutofillHints.password],
      decoration: const InputDecoration(labelText: 'Password'),
    );
  }
}
```

## 일관된 도움말

```dart
/// 각 Scaffold의 appBar.actions에 사용해 도움말이
/// 화면마다 같은 상대 위치에 나타나게 한다.
class ConsistentHelpAction extends StatelessWidget {
  const ConsistentHelpAction({super.key});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.help_outline),
      tooltip: 'Help',
      onPressed: () => Navigator.of(context).pushNamed('/help'),
    );
  }
}
```

## 의미 레이블 테스트

```dart
testWidgets('Close button announces its purpose', (tester) async {
  await tester.pumpWidget(const _Subject());
  expect(find.bySemanticsLabel('Close dialog'), findsOneWidget);
});
```

## 대상 크기 테스트

크기 외 예외와 간격 기준도 함께 확인한다.

```dart
testWidgets('Icon buttons are >= 24 dp on each axis', (tester) async {
  await tester.pumpWidget(const _Subject());
  final size = tester.getSize(find.byIcon(Icons.close).hitTestable());
  expect(size.width, greaterThanOrEqualTo(24));
  expect(size.height, greaterThanOrEqualTo(24));
});
```

## 드래그 대안 테스트

```dart
testWidgets('Dismissible exposes a delete button', (tester) async {
  await tester.pumpWidget(const _Subject());
  expect(find.byTooltip('Delete Item one'), findsOneWidget);
});
```

## 모션 감소 테스트

```dart
testWidgets('Hero is skipped when disableAnimations is true', (tester) async {
  await tester.pumpWidget(
    MediaQuery(
      data: const MediaQueryData(accessibleNavigation: true, disableAnimations: true),
      child: const _Subject(),
    ),
  );
  expect(find.byType(Hero), findsNothing);
});
```
