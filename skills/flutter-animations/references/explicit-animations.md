# 명시적 애니메이션 패턴

암시적 방식으로 요구사항을 충족하지 못할 때 읽는다.

## 컨트롤러 구성

```dart
class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(duration: Durations.medium2, vsync: this);
    _fadeAnimation = _controller.drive(CurveTween(curve: Easing.standard));
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
        return Opacity(opacity: _fadeAnimation.value, child: child);
      },
      child: widget.child, // State 예제: 위젯이 제공하는 정적 자식이다.
    );
  }
}
```

한 개면 `SingleTickerProviderStateMixin`, 여러 개면 `TickerProviderStateMixin`을 사용한다.

## Interval 시간차

하나의 컨트롤러에서 슬라이드가 페이드 중간에 시작하도록 구간을 나눈다. 동시에 목표 값으로 이동하는 속성이라면 암시적 위젯 조합을 먼저 고려한다.

```dart
late final Animation<double> _fadeAnimation = _controller.drive(
  CurveTween(curve: const Interval(0.0, 0.5, curve: Easing.standard)),
);

late final Animation<Offset> _slideAnimation =
    Tween<Offset>(begin: const Offset(0, 0.25), end: Offset.zero).animate(
      _controller.drive(
        CurveTween(
          curve: const Interval(
            0.2,
            0.8,
            curve: Curves.easeInOutCubicEmphasized,
          ),
        ),
      ),
    );
```

## 위젯 갱신에 반응

속성 변경은 `didUpdateWidget`에서 시작·중지·역재생으로 연결한다. 최초 재생은 `initState`에서 시작하고 `build()`에서 시작하지 않는다.

```dart
class _AnimatedGlowState extends State<AnimatedGlow>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(duration: Durations.long2, vsync: this);
    if (widget.isGlowing) {
      _controller.repeat(reverse: true);
    }
  }

  @override
  void didUpdateWidget(AnimatedGlow oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isGlowing != oldWidget.isGlowing) {
      if (widget.isGlowing) {
        _controller.repeat(reverse: true);
      } else {
        _controller.stop();
        _controller.reset();
      }
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  // ...
}
```

## 테스트를 위한 컨트롤러 주입

선택적 생성자 매개변수로 컨트롤러를 받으면 테스트에서 직접 진행시킬 수 있다.

```dart
class const PulsingDot({
  required final bool isActive,
  super.key,
  @visibleForTesting final AnimationController? controller,
}) extends StatefulWidget {
  @override
  State<PulsingDot> createState() => _PulsingDotState();
}

class _PulsingDotState extends State<PulsingDot>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  bool _ownsController = false;

  @override
  void initState() {
    super.initState();
    if (widget.controller != null) {
      _controller = widget.controller!;
    } else {
      _ownsController = true;
      _controller = AnimationController(duration: Durations.long2, vsync: this);
    }
  }

  @override
  void dispose() {
    if (_ownsController) {
      _controller.dispose();
    }
    super.dispose();
  }

  // ...
}
```

위젯이 생성한 컨트롤러만 위젯에서 해제한다. 주입한 컨트롤러는 주입자가 수명을 관리한다. 이 조각은 초기 주입만 보여 준다. 동일 State에서 controller 변경을 지원하려면 didUpdateWidget에서 기존 연결 해제·소유 컨트롤러 해제·새 연결을 구현한다. 여러 티커를 순차 생성할 수 있으면 TickerProviderStateMixin을 사용한다.

## 전환 위젯과 AnimatedBuilder

속성 하나면 내장 전환 위젯을 직접 사용한다.

```dart
// 좋은 예: 속성 하나는 전환 위젯 사용
FadeTransition(
  opacity: _fadeAnimation,
  child: child,
)
```

여러 속성을 명시적으로 조합할 때 `AnimatedBuilder`를 사용한다.

```dart
// 좋은 예: 명시적 여러 속성 조합에 AnimatedBuilder 사용
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Opacity(
      opacity: _fadeAnimation.value,
      child: SlideTransition(
        position: _slideAnimation,
        child: child,
      ),
    );
  },
  child: child,
)
```

| 상황 | 선택 |
| --- | --- |
| 불투명도·위치·배율·회전 중 하나 | `FadeTransition`, `SlideTransition`, `ScaleTransition`, `RotationTransition` |
| 여러 속성 조합 | `AnimatedBuilder` |

특정 위젯과 애니메이션을 강하게 묶는 `AnimatedWidget` 상속은 재사용성을 고려해 신중히 선택한다.
