---
name: flutter-animations
description: "Flutter 애니메이션·모션·화면 전환을 구현하거나 검토할 때 사용한다. 암시적 애니메이션, 컨트롤러, Material 3 모션, Hero를 다룬다."
---

# Flutter 애니메이션

Flutter 내장 애니메이션과 Material 3 모션을 다룬다. Lottie·Rive 전용 작업에는 별도 지침이 필요하다.

## 핵심 기준

- 시각적 의도가 불명확하면 바뀔 속성, 트리거, 시간, 곡선 중 필요한 정보만 확인한다. 충분한 사양이 있으면 바로 구현한다.
- 목표 값으로 이동하는 동작은 암시적 애니메이션을 기본으로 한다. 재생·정지·역재생·반복 또는 시간차 제어가 필요할 때 컨트롤러를 쓴다. 사용자가 구현 방식을 지정했다면 그 선택을 존중하고 필요한 절충점을 설명한다.
- 새 모션은 `Durations`와 `Easing` 토큰을 사용한다. 명시적인 디자인 사양이 있으면 그 값을 이름 있는 상수로 관리한다.
- 여러 기능에서 쓰는 시간·곡선·오프셋은 `AppMotion` 등에 모은다.
- 소유한 `AnimationController`는 `super.dispose()` 전에 해제한다. 하나면 `SingleTickerProviderStateMixin`, 여러 개면 `TickerProviderStateMixin`을 쓴다.
- 애니메이션 빌더에는 바뀌는 하위 트리만 넣는다. 위치·크기의 시각적 변화는 가능한 한 `Transform`을 활용한다. `width`, `height`, `padding`의 매 프레임 변경은 레이아웃 비용을 유발하므로 실제 레이아웃 변화가 필요할 때만 쓴다.
- Dart 3.13 이상이면 기본 생성자의 선언 매개변수를 사용하고, 이전 버전에서는 호환 문법을 유지한다.

## 선택 기준

```text
값이 바뀔 때 위젯이 재빌드되는가?
  ├─ 예: 해당 AnimatedFoo가 있는가?
  │      ├─ 예: 암시적 AnimatedFoo 사용
  │      └─ 아니오: TweenAnimationBuilder 사용
  └─ 아니오: 반복·역재생·순차 진행·상태 감시가 필요한가?
         ├─ 예: AnimationController와 전환 위젯/AnimatedBuilder
         └─ 아니오: TweenAnimationBuilder 검토
```

여러 속성이 동시에 같은 트리거로 목표 값에 이동하는 경우도 암시적 애니메이션이다. 페이드와 슬라이드를 함께 실행하려고 컨트롤러를 만들 필요는 없다. 두 번째 동작이 첫 번째의 중간에 시작하거나 재생 제어가 필요하면 명시적 애니메이션을 선택한다.

## Material 3 모션 토큰

프레임워크의 `Durations`·`Easing`을 기본으로 사용한다.

```dart
// 나쁜 예: 의미 없는 임의 값
AnimatedContainer(
  duration: Duration(milliseconds: 375),
  curve: Curves.easeInOutCubic,
)

// 좋은 예: 의도가 드러나는 Material 3 토큰
AnimatedContainer(
  duration: Durations.medium2,
  curve: Easing.standard,
)
```

여러 기능이 공유할 때 `AppMotion`으로 묶는다. 한 곳뿐이면 토큰을 직접 참조해도 된다.

```dart
abstract class AppMotion {
  // 일반 전환
  static const Duration standardDuration = Durations.medium2;
  static const Curve standardCurve = Easing.standard;

  // 화면 전환
  static const Duration pageDuration = Durations.medium4;
  static const Curve pageEnterCurve = Easing.emphasizedDecelerate;
  static const Curve pageExitCurve = Easing.emphasizedAccelerate;

  // 페이드
  static const Duration fadeDuration = Durations.short3;
  static const Curve fadeCurve = Easing.standard;
}
```

## 암시적 애니메이션

새 목표 값으로 재빌드하면 프레임워크가 보간한다. `AnimatedOpacity`, `AnimatedSlide`, `AnimatedSwitcher`처럼 해당 속성의 위젯을 사용한다. 여러 속성은 조합한다.

```dart
class const SummaryCard({required final Summary? summary, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final hasData = summary != null;

    return AnimatedOpacity(
      opacity: hasData ? 1 : 0,
      duration: Durations.medium2,
      curve: Easing.standard,
      child: AnimatedSlide(
        offset: hasData ? Offset.zero : const Offset(0, 0.1),
        duration: Durations.medium2,
        curve: Easing.emphasizedDecelerate,
        child: Card(child: _SummaryContents(summary: summary)),
      ),
    );
  }
}
```

두 속성이 같은 재빌드에서 움직인다. 컨트롤러·티커·해제 코드는 필요하지 않다.

## TweenAnimationBuilder

해당 속성의 내장 위젯이 없을 때 사용한다. 값에 의존하지 않는 위젯은 `child`로 전달해 매 프레임 재빌드를 피한다.

```dart
TweenAnimationBuilder<double>(
  tween: Tween(begin: 0, end: isActive ? 1.0 : 0.0),
  duration: Durations.medium2,
  curve: Easing.standard,
  builder: (context, value, child) {
    return Transform.scale(
      scale: 0.8 + (0.2 * value),
      child: Opacity(
        opacity: value,
        child: child,
      ),
    );
  },
  child: child, // 변하지 않는 child는 재빌드하지 않는다.
)
```

## 명시적 애니메이션

재생·정지·역재생·반복 또는 상태 감지가 필요하면 컨트롤러를 사용한다.

```dart
class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Durations.medium2,
      vsync: this,
    );
    _fadeAnimation = CurvedAnimation(
      parent: _controller,
      curve: Easing.standard,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _fadeAnimation,
      builder: (context, child) {
        return Opacity(
          opacity: _fadeAnimation.value,
          child: child,
        );
      },
      child: child, // 정적 자식은 매 프레임 재빌드하지 않는다.
    );
  }
}
```

[컨트롤러 패턴](references/explicit-animations.md)에서 `didUpdateWidget`, 주입과 소유권, 전환 위젯 선택을 확인한다.

### Interval로 시간차 주기

하나의 컨트롤러에서 `CurvedAnimation`의 `Interval`로 시작 구간을 나눈다. 같은 시점에 목표 값으로 움직이는 여러 속성과 구분한다.

```dart
late final Animation<double> _fadeAnimation = CurvedAnimation(
  parent: _controller,
  curve: const Interval(0.0, 0.5, curve: Easing.standard),
);

late final Animation<Offset> _slideAnimation = Tween<Offset>(
  begin: const Offset(0, 0.25),
  end: Offset.zero,
).animate(
  CurvedAnimation(
    parent: _controller,
    curve: const Interval(0.2, 0.8, curve: Easing.emphasized),
  ),
);
```

[시간차 예제](references/staggered-animations.md)와 [반복 예제](references/looping-animations.md)를 필요할 때 읽는다.

## 화면 전환

`GoRouteData.buildPage`의 `CustomTransitionPage`로 통합한다. 여러 라우트가 공유하면 `AppPageTransitions`로 추출한다. [전환과 Hero](references/page-transitions.md)를 참고한다.

## 성능과 피해야 할 패턴

- 시각적 위치·배율에는 `Transform`, 페이드에는 적절한 불투명도 위젯을 쓴다. 레이아웃 비용을 줄일 수 있지만 합성·래스터 비용은 실제 화면에서 확인한다.
- `AnimatedBuilder`·`TweenAnimationBuilder`의 `child`로 정적 하위 트리를 분리한다.
- 복잡한 화면에서는 `RepaintBoundary`의 효과를 측정한다.
- 전체 화면을 빌더로 감싸거나 같은 시간축에 여러 컨트롤러를 만들지 않는다.

### 크기 변경과 Transform 비교

```dart
// 나쁜 예: 매 프레임 SizedBox와 하위 트리의 레이아웃 수행
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return SizedBox(
      width: 200 + (_controller.value * 120),
      child: child,
    );
  },
  child: const ExpensiveChart(),
)

// 좋은 예: Transform.scale로 레이아웃 변경을 피한다.
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform.scale(
      scaleX: 1 + (_controller.value * 0.6),
      child: child,
    );
  },
  child: const ExpensiveChart(),
)
```

크기 애니메이션으로 매 프레임 레이아웃이 발생한다면 `Transform.scale`·`Transform.translate`로 요구사항을 충족할 수 있는지 검토한다.

### 정적 자식의 반복 빌드

```dart
// 나쁜 예: 전체 하위 트리를 매 프레임 재빌드
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Opacity(
      opacity: _controller.value,
      child: const ExpensiveWidget(), // 매 프레임 재빌드됨
    );
  },
)
```

### 암시적 방식으로 충분한 경우

```dart
// 나쁜 예: 단순 목표 값 애니메이션에 불필요한 복잡성
class _FadeWidgetState extends State<FadeWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  // 추가적인 초기화·해제 코드

// 좋은 예: 위젯 하나로 표현
AnimatedOpacity(
  duration: Durations.short3,
  curve: Easing.standard,
  opacity: isVisible ? 1.0 : 0.0,
  child: child,
)
```

단순 불리언 페이드는 `AnimatedOpacity`로 충분하다. 명시적 컨트롤러를 요청한 사용자에게는 이유를 짧게 설명하되 사용자의 선택을 무시하지 않는다.

## 참고 문서

- [암시적 애니메이션](references/implicit-animations.md)
- [명시적 애니메이션](references/explicit-animations.md)
- [시간차 애니메이션](references/staggered-animations.md)
- [화면 전환](references/page-transitions.md)
- [반복 애니메이션](references/looping-animations.md)
