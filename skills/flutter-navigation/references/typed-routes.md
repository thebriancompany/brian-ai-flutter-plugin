# 타입 안전한 라우트

`GoRouteData`와 `@TypedGoRoute`로 오타·수동 캐스팅을 줄인다. `go_router_builder`를 설정하고 `dart run build_runner build --delete-conflicting-outputs`로 헬퍼를 생성한다.

## 기본 라우트

```dart
@TypedGoRoute<CategoriesPageRoute>(
  name: 'categories',
  path: '/categories',
)
@immutable
class const CategoriesPageRoute({
  final String? size,
  final String? color,
}) extends GoRouteData {
  @override
  Widget build(BuildContext context, GoRouterState state) {
    return CategoriesPage(size: size, color: color);
  }
}
```

## 하위 라우트

부모의 routes에 중첩해 URL과 페이지 계층을 일치시킨다.

```dart
@TypedGoRoute<FlutterPageRoute>(
  name: 'flutter',
  path: '/flutter',
  routes: [
    TypedGoRoute<FlutterNewsPageRoute>(
      name: 'flutterNews',
      path: 'news',
    ),
    TypedGoRoute<FlutterArticlesPageRoute>(
      name: 'flutterArticles',
      path: 'articles',
      routes: [
        TypedGoRoute<FlutterArticlePageRoute>(
          name: 'flutterArticle',
          path: 'article/:id',
        ),
      ],
    ),
  ],
)
@immutable
class FlutterPageRoute extends GoRouteData {
  const FlutterPageRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const FlutterPage();
  }
}
```

## 셸 라우트

하단 탭·내비게이션 레일 등 여러 화면에 유지되는 외곽 UI에 `TypedShellRoute`를 사용한다.

```dart
@TypedShellRoute<AppShellRoute>(
  routes: [
    TypedGoRoute<HomePageRoute>(
      name: 'home',
      path: '/home',
    ),
    TypedGoRoute<SettingsPageRoute>(
      name: 'settings',
      path: '/settings',
    ),
  ],
)
class AppShellRoute extends ShellRouteData {
  @override
  Widget builder(BuildContext context, GoRouterState state, Widget navigator) {
    return AppShell(child: navigator);
  }
}
```
