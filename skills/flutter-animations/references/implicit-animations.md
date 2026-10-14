# 암시적 애니메이션 패턴

목표 값 변경에 따른 보간은 암시적 애니메이션을 기본으로 한다. 컨트롤러와 티커를 직접 관리하지 않는다.

## 내장 위젯

`AnimatedContainer`, `AnimatedOpacity`, `AnimatedSlide`, `AnimatedAlign`, `AnimatedPadding`, `AnimatedPositioned`, `AnimatedSwitcher` 중 속성에 맞는 것을 선택한다. 레이아웃 속성은 매 프레임 레이아웃 비용도 고려한다.

## 여러 속성 조합

데이터가 도착하면 나타나며 이동하는 위젯처럼, 동시에 변하는 속성은 각 암시적 위젯을 조합한다.

```dart
class const SummaryCard({required final Summary? summary, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final hasData = summary != null;
    final duration = MediaQuery.disableAnimationsOf(context)
        ? Duration.zero
        : Durations.medium2;

    return AnimatedOpacity(
      opacity: hasData ? 1 : 0,
      duration: duration,
      curve: Easing.standard,
      child: AnimatedSlide(
        offset: hasData ? Offset.zero : const Offset(0, 0.1),
        duration: duration,
        curve: Easing.emphasizedDecelerate,
        child: Card(child: _SummaryContents(summary: summary)),
      ),
    );
  }
}
```

두 속성이 같은 재빌드에서 시작한다.

## TweenAnimationBuilder

해당 속성의 내장 위젯이 없다면 사용한다.

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

애니메이션 값과 무관한 위젯은 `child`로 전달해 한 번만 빌드한다.
