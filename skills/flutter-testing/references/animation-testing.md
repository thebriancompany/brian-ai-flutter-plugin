# 애니메이션 테스트

구현 방식은 [애니메이션 스킬](../../flutter-animations/SKILL.md)을 참고한다.

## 암시적 애니메이션

구체적인 시간만큼 `pump`해 중간·최종 상태를 검증한다.

```dart
testWidgets('card fades in when visible', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: FadingCard(isVisible: false),
    ),
  );

  // 초기 상태 검증
  final opacity = tester.widget<AnimatedOpacity>(
    find.byType(AnimatedOpacity),
  );
  expect(opacity.opacity, 0.0);

  // 애니메이션 시작
  await tester.pumpWidget(
    const MaterialApp(
      home: FadingCard(isVisible: true),
    ),
  );

  // 목표 값 설정 확인
  final updatedOpacity = tester.widget<AnimatedOpacity>(
    find.byType(AnimatedOpacity),
  );
  expect(updatedOpacity.opacity, 1.0);

  // 애니메이션 완료까지 진행
  await tester.pumpAndSettle();

  // 최종 렌더링 상태 검증
  final renderOpacity = tester.renderObject<RenderAnimatedOpacity>(
    find.byType(AnimatedOpacity),
  );
  expect(renderOpacity.opacity.value, 1.0);
});
```

## 명시적 애니메이션

프레임 시간을 진행해 동작을 검증한다.

```dart
testWidgets('spinner rotates continuously', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(home: Spinner()),
  );

  // 초기 변환 기록
  final initialTransform = tester.widget<Transform>(
    find.byType(Transform),
  );

  // 한 프레임 진행
  await tester.pump();

  // 회전이 진행되었는지 검증
  final updatedTransform = tester.widget<Transform>(
    find.byType(Transform),
  );
  expect(updatedTransform.transform, isNot(initialTransform.transform));
});
```

## AnimatedSwitcher

```dart
testWidgets('content cross-fades on state change', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: CounterDisplay(count: 0),
    ),
  );

  expect(find.text('0'), findsOneWidget);

  await tester.pumpWidget(
    const MaterialApp(
      home: CounterDisplay(count: 1),
    ),
  );

  // 교차 페이드 중에는 두 위젯이 함께 존재한다.
  await tester.pump(Durations.medium2 ~/ 2);
  expect(find.text('0'), findsOneWidget);
  expect(find.text('1'), findsOneWidget);

  // 완료 후에는 새 위젯만 남는다.
  await tester.pumpAndSettle();
  expect(find.text('0'), findsNothing);
  expect(find.text('1'), findsOneWidget);
});
```

## 화면 전환

```dart
testWidgets('details page slides in from right', (tester) async {
  final router = GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        builder: (_, __) => const HomePage(),
      ),
      GoRoute(
        path: '/details',
        pageBuilder: (context, state) => AppPageTransitions.slideFade(
          key: state.pageKey,
          child: const DetailsPage(),
        ),
      ),
    ],
  );

  await tester.pumpWidget(
    MaterialApp.router(routerConfig: router),
  );

  router.go('/details');
  await tester.pump();
  await tester.pump(Durations.medium4 ~/ 2);

  // 전환 중인 상세 화면은 존재하지만 아직 안정화되지 않았다.
  expect(find.byType(DetailsPage), findsOneWidget);

  await tester.pumpAndSettle();
  expect(find.byType(DetailsPage), findsOneWidget);
  expect(find.byType(HomePage), findsNothing);
});
```

## 컨트롤러 주입

위젯이 테스트용 선택적 컨트롤러를 제공하면 테스트가 직접 진행시킨다.

```dart
testWidgets('pulsing dot scales when active', (tester) async {
  final controller = AnimationController(
    duration: Durations.long2,
    vsync: const TestVSync(),
  );
  addTearDown(controller.dispose);

  await tester.pumpWidget(
    MaterialApp(
      home: PulsingDot(
        isActive: true,
        controller: controller,
      ),
    ),
  );

  // 애니메이션 중간까지 진행
  controller.value = 0.5;
  await tester.pump();

  final transform = tester.widget<Transform>(find.byType(Transform));
  // 배율이 시작과 끝 사이인지 검증
  expect(transform.transform.getMaxScaleOnAxis(), greaterThan(1.0));

  // 완료까지 진행
  controller.value = 1.0;
  await tester.pump();

  final finalTransform = tester.widget<Transform>(find.byType(Transform));
  expect(finalTransform.transform.getMaxScaleOnAxis(), closeTo(1.05, 0.01));
});
```

`forward()`·`reverse()`·`repeat()` 호출 자체가 계약이면 mocktail로 검증한다.

```dart
class MockAnimationController extends Mock implements AnimationController {}

testWidgets('stops animation when isActive becomes false', (tester) async {
  final controller = MockAnimationController();
  when(() => controller.repeat(reverse: true)).thenReturn();
  when(() => controller.stop()).thenReturn();
  when(() => controller.reset()).thenReturn();
  when(() => controller.value).thenReturn(0.0);
  when(() => controller.status).thenReturn(AnimationStatus.dismissed);

  await tester.pumpWidget(
    MaterialApp(
      home: PulsingDot(isActive: true, controller: controller),
    ),
  );
  verify(() => controller.repeat(reverse: true)).called(1);

  await tester.pumpWidget(
    MaterialApp(
      home: PulsingDot(isActive: false, controller: controller),
    ),
  );
  verify(() => controller.stop()).called(1);
  verify(() => controller.reset()).called(1);
});
```

## 주의점

- 유한한 애니메이션만 `pumpAndSettle`로 완료를 기다린다. 첫 인수는 제한 시간이 아니라 펌프 간격이다. 제한은 세 번째 위치 인수이며 예를 들어 `await tester.pumpAndSettle(const Duration(milliseconds: 100), EnginePhase.sendSemanticsUpdate, const Duration(seconds: 5))`로 지정한다.
- 중간 시점은 `pump(duration)`으로 검증한다.
- 변환의 정확한 픽셀보다 방향·완료 여부를 검증한다.
- 반복 애니메이션은 명시적인 시간의 `pump`만 사용한다.
