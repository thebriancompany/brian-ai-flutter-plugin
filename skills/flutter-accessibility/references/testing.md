# 접근성 테스트 예제

의미 정보·대상 크기·포커스·대비·텍스트 확대·모션·폼을 검증한다. 아래는 앱의 위젯과 헬퍼에 맞춰 수정할 예제이며 자동 검사만으로 전체 WCAG 준수를 인증하지 않는다. Android 48dp·iOS 44pt 검사와 WCAG AA 최소 기준을 구분한다. 의미 플래그 검사는 실제 화면 낭독의 발화를 증명하지 않는다. `findsOneWidget`만으로 텍스트 잘림이나 모션 감소가 검증되었다고 보고하지 않는다.

```dart
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  // --- A. 의미 정보와 화면 낭독 ---
  group('Semantics', () {
    testWidgets('informational image exposes a label', (tester) async {
      final handle = tester.ensureSemantics();
      try {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: Semantics(
                image: true,
                label: 'Company logo',
                child: const SizedBox(width: 48, height: 48),
              ),
            ),
          ),
        );

        final semantics = tester.getSemantics(
          find.bySemanticsLabel('Company logo'),
        );
        expect(semantics.label, isNotEmpty);
      } finally {
        handle.dispose();
      }
    });

    testWidgets('icon buttons have tooltips', (tester) async {
      final handle = tester.ensureSemantics();
      try {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: IconButton(
                icon: const Icon(Icons.search),
                tooltip: 'Search',
                onPressed: () {},
              ),
            ),
          ),
        );

        expect(find.byTooltip('Search'), findsOneWidget);
      } finally {
        handle.dispose();
      }
    });

    testWidgets('status exposes live region semantics', (tester) async {
      final handle = tester.ensureSemantics();
      try {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: Semantics(
                liveRegion: true,
                child: const Text('Loading complete'),
              ),
            ),
          ),
        );

        final semantics = tester.getSemantics(find.text('Loading complete'));
        expect(semantics.flagsCollection.isLiveRegion, isTrue);
      } finally {
        handle.dispose();
      }
    });
  });

  // --- B. 조작 대상 크기 ---
  group('Touch targets', () {
    testWidgets('icon button meets 48dp minimum', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Center(
              child: IconButton(
                icon: const Icon(Icons.close),
                onPressed: () {},
              ),
            ),
          ),
        ),
      );

      final size = tester.getSize(find.byType(IconButton));
      expect(size.width, greaterThanOrEqualTo(48));
      expect(size.height, greaterThanOrEqualTo(48));
    });

    testWidgets('text button meets 48dp minimum height', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Center(
              child: TextButton(onPressed: () {}, child: const Text('Action')),
            ),
          ),
        ),
      );

      final size = tester.getSize(find.byType(TextButton));
      expect(size.height, greaterThanOrEqualTo(48));
    });
  });

  // --- C. 포커스와 키보드 ---
  group('Focus management', () {
    testWidgets('dialog traps focus', (tester) async {
      final cancelFocus = FocusNode();
      final confirmFocus = FocusNode();
      addTearDown(cancelFocus.dispose);
      addTearDown(confirmFocus.dispose);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Builder(
              builder: (context) => ElevatedButton(
                onPressed: () => showDialog<void>(
                  context: context,
                  builder: (_) => AlertDialog(
                    title: const Text('Confirm'),
                    content: const Text('Are you sure?'),
                    actions: [
                      TextButton(
                        focusNode: cancelFocus,
                        autofocus: true,
                        onPressed: () {},
                        child: const Text('Cancel'),
                      ),
                      TextButton(
                        focusNode: confirmFocus,
                        onPressed: () {},
                        child: const Text('OK'),
                      ),
                    ],
                  ),
                ),
                child: const Text('Open'),
              ),
            ),
          ),
        ),
      );

      await tester.tap(find.text('Open'));
      await tester.pumpAndSettle();

      expect(find.text('Confirm'), findsOneWidget);

      void expectDialogFocus(FocusNode expected) {
        final primaryFocus = FocusManager.instance.primaryFocus;
        expect(primaryFocus, same(expected));
        expect(
          primaryFocus!.context!.findAncestorWidgetOfExactType<AlertDialog>(),
          isNotNull,
        );
      }

      expectDialogFocus(cancelFocus);

      // Tab으로 마지막 버튼을 지나도 대화상자 안에서 순환한다.
      for (final expected in [confirmFocus, cancelFocus]) {
        await tester.sendKeyEvent(LogicalKeyboardKey.tab);
        await tester.pumpAndSettle();
        expectDialogFocus(expected);
      }

      // Shift+Tab으로 첫 버튼을 지나 역방향 순환도 검증한다.
      await tester.sendKeyDownEvent(LogicalKeyboardKey.shiftLeft);
      try {
        for (final expected in [confirmFocus, cancelFocus]) {
          await tester.sendKeyEvent(LogicalKeyboardKey.tab);
          await tester.pumpAndSettle();
          expectDialogFocus(expected);
        }
      } finally {
        await tester.sendKeyUpEvent(LogicalKeyboardKey.shiftLeft);
      }
    });

    testWidgets('button and link can be activated with keyboard', (
      tester,
    ) async {
      var buttonActivations = 0;
      var linkActivations = 0;
      final buttonFocus = FocusNode();
      final linkFocus = FocusNode();
      addTearDown(buttonFocus.dispose);
      addTearDown(linkFocus.dispose);
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Column(
              children: [
                ElevatedButton(
                  focusNode: buttonFocus,
                  onPressed: () => buttonActivations++,
                  child: const Text('Button'),
                ),
                InkWell(
                  focusNode: linkFocus,
                  onTap: () => linkActivations++,
                  child: const Text('Link'),
                ),
              ],
            ),
          ),
        ),
      );
      buttonFocus.requestFocus();
      await tester.pump();
      await tester.sendKeyEvent(LogicalKeyboardKey.enter);
      expect(buttonActivations, 1);
      linkFocus.requestFocus();
      await tester.pump();
      await tester.sendKeyEvent(LogicalKeyboardKey.enter);
      expect(linkActivations, 1);
    });
  });

  // --- D. 색상 대비 ---
  group('Color contrast', () {
    testWidgets('error state uses icon and label, not just color', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: Row(
              children: [
                Icon(Icons.error, color: Colors.red),
                SizedBox(width: 8),
                Text('Invalid input'),
              ],
            ),
          ),
        ),
      );

      // 색뿐 아니라 아이콘과 텍스트가 함께 존재한다.
      expect(find.byIcon(Icons.error), findsOneWidget);
      expect(find.text('Invalid input'), findsOneWidget);
    });
  });

  // --- E. 글자 확대 ---
  group('Text scaling', () {
    testWidgets('text container uses minHeight, not fixed height', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ConstrainedBox(
              constraints: const BoxConstraints(minHeight: 48),
              child: const Text('Scalable text'),
            ),
          ),
        ),
      );

      // 기본 배율에서 위젯이 렌더링된다.
      expect(find.text('Scalable text'), findsOneWidget);
    });

    testWidgets('text lays out without truncation at 2x scale', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(context)
                .copyWith(textScaler: const TextScaler.linear(2)),
            child: child!,
          ),
          home: const Scaffold(
            body: SizedBox(
              width: 240,
              child: SingleChildScrollView(
                child: Text('This text should wrap without being clipped'),
              ),
            ),
          ),
        ),
      );
      final finder = find.text('This text should wrap without being clipped');
      final paragraph = tester.renderObject<RenderParagraph>(finder);
      expect(paragraph.textScaler.scale(16), 32);
      expect(paragraph.didExceedMaxLines, isFalse);
      expect(tester.takeException(), isNull);
      // 상위 Stack·ClipRect 등의 잘림과 실제 화면 낭독은 별도 화면 검증이 필요하다.
    });
  });

  // --- F. 애니메이션과 모션 ---
  group('Animation & motion', () {
    testWidgets('reduced motion selects zero duration', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(context).copyWith(disableAnimations: true),
            child: child!,
          ),
          home: Scaffold(
            body: Builder(
              builder: (context) => AnimatedContainer(
                duration: MediaQuery.disableAnimationsOf(context)
                    ? Duration.zero
                    : const Duration(milliseconds: 300),
                color: Colors.blue,
                child: const Text('Animated'),
              ),
            ),
          ),
        ),
      );
      expect(
        tester
            .widget<AnimatedContainer>(find.byType(AnimatedContainer))
            .duration,
        Duration.zero,
      );
    });
  });
}
```
