# 리다이렉트

전역 라우터와 개별 라우트에 적용할 수 있다. 부모·자식 접근 조건과 인증 변경에 따른 재평가, 순환 여부를 테스트한다.

## 전역 인증 검사

```dart
GoRouter _routes(GlobalKey<NavigatorState> navigatorKey) {
  return GoRouter(
    initialLocation: '/',
    navigatorKey: navigatorKey,
    redirect: (context, state) {
      final status = context.read<AppBloc>().state.status;
      if (status == AppStatus.unauthenticated) {
        return SignInPageRoute().location;
      }
      return null;
    },
    routes: $appRoutes,
  );
}
```

## 라우트 권한 검사

```dart
@TypedGoRoute<PremiumPageRoute>(
  name: 'premium',
  path: '/premium',
  routes: [
    TypedGoRoute<PremiumShowsPageRoute>(
      name: 'premiumShows',
      path: 'shows',
    ),
  ],
)
class PremiumPageRoute extends GoRouteData {
  @override
  String? redirect(BuildContext context, GoRouterState state) {
    final status = context.read<AppBloc>().state.user.status;
    if (status != UserStatus.premium) {
      return RestrictedPageRoute().location;
    }
    return null;
  }

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const PremiumPage();
  }
}
```
