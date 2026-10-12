# 시간차 애니메이션

하나의 컨트롤러에서 `Interval`로 각 애니메이션이 활성화될 시간 비율을 지정한다.

## 페이드·슬라이드·배율의 시간차 진입

```dart
class _StaggeredEntryState extends State<StaggeredEntry>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _fadeAnimation;
  late final Animation<Offset> _slideAnimation;
  late final Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Durations.long2,
      vsync: this,
    );

    _fadeAnimation = CurvedAnimation(
      parent: _controller,
      curve: const Interval(0.0, 0.6, curve: Easing.standard),
    );

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.15),
      end: Offset.zero,
    ).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.1, 0.7, curve: Easing.emphasized),
      ),
    );

    _scaleAnimation = Tween<double>(begin: 0.95, end: 1.0).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.1, 0.7, curve: Easing.emphasized),
      ),
    );

    _controller.forward();
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
        return Opacity(
          opacity: _fadeAnimation.value,
          child: SlideTransition(
            position: _slideAnimation,
            child: ScaleTransition(
              scale: _scaleAnimation,
              child: child,
            ),
          ),
        );
      },
      child: widget.child,
    );
  }
}
```

## 목록 항목 순차 진입

항목마다 지연을 달리한다.

```dart
class const StaggeredListItem({
  required final int index,
  required final int itemCount,
  required final Animation<double> animation,
  required final Widget child,
  super.key,
}) extends StatefulWidget {
  @override
  State<StaggeredListItem> createState() => _StaggeredListItemState();
}

class _StaggeredListItemState extends State<StaggeredListItem> {
  late final CurvedAnimation _curvedAnimation;

  @override
  void initState() {
    super.initState();
    final start = (widget.index / widget.itemCount).clamp(0.0, 1.0);
    final end = ((widget.index + 1) / widget.itemCount).clamp(0.0, 1.0);
    _curvedAnimation = CurvedAnimation(
      parent: widget.animation,
      curve: Interval(start, end, curve: Easing.emphasized),
    );
  }

  @override
  void dispose() {
    _curvedAnimation.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _curvedAnimation,
      child: SlideTransition(
        position: Tween<Offset>(
          begin: const Offset(0, 0.1),
          end: Offset.zero,
        ).animate(_curvedAnimation),
        child: widget.child,
      ),
    );
  }
}
```

부모 컨트롤러와 연결한다.

```dart
class _StaggeredListState extends State<StaggeredList>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Durations.extralong2,
      vsync: this,
    )..forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final items = widget.items;
    return Column(
      children: [
        for (var i = 0; i < items.length; i++)
          StaggeredListItem(
            index: i,
            itemCount: items.length,
            animation: _controller,
            child: items[i],
          ),
      ],
    );
  }
}
```
