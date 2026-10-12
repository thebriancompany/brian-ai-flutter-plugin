# GoRouter 화면 전환

## 공유 전환 헬퍼

여러 라우트가 같은 전환을 사용할 때 추출한다.

```dart
abstract class AppPageTransitions {
  static CustomTransitionPage<void> fade({
    required LocalKey key,
    required Widget child,
  }) {
    return CustomTransitionPage(
      key: key,
      child: child,
      transitionDuration: Durations.medium4,
      reverseTransitionDuration: Durations.medium4,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(
          opacity: CurvedAnimation(
            parent: animation,
            curve: Easing.emphasizedDecelerate,
          ),
          child: child,
        );
      },
    );
  }

  static CustomTransitionPage<void> slideFade({
    required LocalKey key,
    required Widget child,
  }) {
    return CustomTransitionPage(
      key: key,
      child: child,
      transitionDuration: Durations.medium4,
      reverseTransitionDuration: Durations.medium4,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        final curvedAnimation = CurvedAnimation(
          parent: animation,
          curve: Easing.emphasizedDecelerate,
        );
        return FadeTransition(
          opacity: curvedAnimation,
          child: SlideTransition(
            position: Tween<Offset>(
              begin: const Offset(0.05, 0),
              end: Offset.zero,
            ).animate(curvedAnimation),
            child: child,
          ),
        );
      },
    );
  }

  static CustomTransitionPage<void> slideUp({
    required LocalKey key,
    required Widget child,
  }) {
    return CustomTransitionPage(
      key: key,
      child: child,
      transitionDuration: Durations.medium4,
      reverseTransitionDuration: Durations.medium4,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        final curvedAnimation = CurvedAnimation(
          parent: animation,
          curve: Easing.emphasizedDecelerate,
        );
        return FadeTransition(
          opacity: curvedAnimation,
          child: SlideTransition(
            position: Tween<Offset>(
              begin: const Offset(0, 0.1),
              end: Offset.zero,
            ).animate(curvedAnimation),
            child: child,
          ),
        );
      },
    );
  }
}
```

## GoRouteData 연결

```dart
@TypedGoRoute<DetailsPageRoute>(
  name: 'details',
  path: 'details/:id',
)
@immutable
class const DetailsPageRoute({required final String id}) extends GoRouteData {
  @override
  Page<void> buildPage(BuildContext context, GoRouterState state) {
    return AppPageTransitions.slideFade(
      key: state.pageKey,
      child: DetailsPage(id: id),
    );
  }
}
```

## Hero 공유 요소 전환

출발·도착 라우트에 같은 태그를 부여하면 프레임워크가 전환을 처리한다.

```dart
// 출발 화면
Hero(
  tag: 'product-image-${product.id}',
  child: Image.network(product.imageUrl),
)

// 도착 화면
Hero(
  tag: 'product-image-${product.id}',
  child: Image.network(product.imageUrl),
)
```

- 같은 라우트 안의 태그는 고유해야 한다. 인덱스보다 의미 있는 식별자를 쓴다.
- 전환 시 출발·도착 요소가 존재해야 한다. 지연 목록에서 출발 요소가 제거되는 경우를 확인한다.
- 카드 전체보다 이동할 시각적 요소만 감싼다.
