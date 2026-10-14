# 반복 애니메이션

## 연속 회전 로딩 표시

```dart
class _SpinnerState extends State<Spinner> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (MediaQuery.disableAnimationsOf(context)) {
      _controller.stop();
      _controller.value = 0;
    } else {
      _controller.repeat();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Transform.rotate(
          angle: _controller.value * 2 * pi,
          child: child,
        );
      },
      child: const Icon(Icons.refresh),
    );
  }
}
```

## 역재생을 반복하는 맥박 효과

아래는 보간 설정 조각이다. 반복 시작·정지는 위와 같은 didChangeDependencies에서 모션 감소 설정에 따라 제어하고, dispose에서 컨트롤러를 해제한다.

```dart
@override
void initState() {
  super.initState();
  _controller = AnimationController(duration: Durations.long2, vsync: this);

  _scaleAnimation = Tween<double>(
    begin: 1.0,
    end: 1.05,
  ).animate(_controller.drive(CurveTween(curve: Easing.standard)));
}
```
