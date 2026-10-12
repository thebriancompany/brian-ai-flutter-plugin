# 리다이렉트

전역 라우터와 개별 라우트에 적용할 수 있다. 부모·자식 접근 조건과 인증 변경에 따른 재평가, 순환 여부를 테스트한다.

## 전역 인증 검사

로그인 경로에서는 미인증 사용자를 그대로 두고, 인증된 사용자만 기본 화면으로 보낸다. 쿼리 매개변수가 있어도 로그인 경로를 식별하도록 URI의 경로를 비교한다.

```dart
GoRouter _routes(GlobalKey<NavigatorState> navigatorKey) {
  return GoRouter(
    initialLocation: '/',
    navigatorKey: navigatorKey,
    redirect: (context, state) {
      final status = context.read<AppBloc>().state.status;
      final signInLocation = SignInPageRoute().location;
      final isSigningIn = state.uri.path == Uri.parse(signInLocation).path;

      if (status == AppStatus.unauthenticated) {
        return isSigningIn ? null : signInLocation;
      }
      if (status == AppStatus.authenticated && isSigningIn) {
        return HomePageRoute().location;
      }
      return null;
    },
    routes: $appRoutes,
  );
}
```

`context.read` 자체는 인증 변경을 구독하지 않는다. `AppBloc`의 인증 상태 변경 시 `refreshListenable` 또는 `router.refresh()`로 리다이렉트를 재평가하도록 연결한다.

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
