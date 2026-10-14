# 타입 안전한 라우트

`GoRouteData`와 `@TypedGoRoute`로 오타·수동 캐스팅을 줄인다. `go_router_builder`를 설정하고 `dart run build_runner build --delete-conflicting-outputs`로 헬퍼를 생성한다.

아래는 go_router_builder 4.x 이상의 공개 `with $RouteName` 믹스인을 포함한다. 라우트 라이브러리에 go_router import와 `part 'app_routes.g.dart';`를 선언한다. 3.x는 `with _$RouteName`을 사용한다. 기존 builder 버전의 생성 방식이 다르면 [공식 패키지 안내](https://pub.dev/packages/go_router_builder)에 맞춘다. 예제는 생성기 호환성을 위해 일반 생성자를 사용한다. 최상위 경로는 `/`로 시작하고 중첩 경로는 상대 경로를 쓴다.

## 기본 라우트

```dart
@TypedGoRoute<CategoriesPageRoute>(name: 'categories', path: '/categories')
@immutable
class CategoriesPageRoute extends GoRouteData with $CategoriesPageRoute {
  const CategoriesPageRoute({this.size, this.color});

  final String? size;
  final String? color;

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
    TypedGoRoute<FlutterNewsPageRoute>(name: 'flutterNews', path: 'news'),
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
class FlutterPageRoute extends GoRouteData with $FlutterPageRoute {
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
    TypedGoRoute<HomePageRoute>(name: 'home', path: '/home'),
    TypedGoRoute<SettingsPageRoute>(name: 'settings', path: '/settings'),
  ],
)
class AppShellRoute extends ShellRouteData {
  @override
  Widget builder(BuildContext context, GoRouterState state, Widget navigator) {
    return AppShell(child: navigator);
  }
}
```
