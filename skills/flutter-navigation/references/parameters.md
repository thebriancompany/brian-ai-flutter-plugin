# 매개변수 전략

## 경로: 리소스 식별

```dart
@TypedGoRoute<FlutterArticlePageRoute>(
  name: 'flutterArticle',
  path: 'article/:id',
)
@immutable
class const FlutterArticlePageRoute({required final String id})
    extends GoRouteData {
  @override
  Widget build(BuildContext context, GoRouterState state) {
    return FlutterArticlePage(id: id);
  }
}
```

`FlutterArticlePageRoute(id: article.id).go(context);`로 이동한다.

## 쿼리: 필터·정렬

```dart
@TypedGoRoute<FlutterArticlesPageRoute>(
  name: 'flutterArticles',
  path: 'articles',
)
@immutable
class const FlutterArticlesPageRoute({
  final String? date,
  final String? category,
}) extends GoRouteData {
  @override
  Widget build(BuildContext context, GoRouterState state) {
    return FlutterArticlesPage(
      date: date,
      category: category,
    );
  }
}
```

URL 예: `/flutter/articles?date=07162024&category=all`

## extra와 복원

`extra`는 URL의 일부가 아니다. 웹에서 항상 작동하지 않는다는 뜻은 아니지만, URL만으로 진입하는 딥 링크에서 그 객체를 재구성할 수는 없다. 브라우저 저장에는 직렬화도 고려해야 한다. 복원에 필요한 식별자는 경로·쿼리로 넘기고 도착 화면에서 데이터를 읽는다.
