---
name: flutter-navigation
description: "Flutter go_router의 타입 안전한 라우트, 화면 이동, 매개변수, 리다이렉트와 딥 링크를 구현하거나 테스트할 때 사용한다."
---

# Flutter 내비게이션

`go_router`를 사용하는 앱의 라우팅과 딥 링크를 다룬다. 기존 라우터를 요청 없이 교체하지 않는다. 전환 모션은 [애니메이션](../flutter-animations/SKILL.md)을 함께 참고한다.

공식 권고와 팀 관례의 구분, SDK·언어 버전, 오류·수명 처리는 [공통 기준](../flutter-review/SKILL.md#공식-기준과-프로젝트-관례)을 적용한다.

## 핵심 기준

- `GoRouteData`와 `@TypedGoRoute`·`go_router_builder`로 타입 안전한 라우트와 생성된 이동 메서드를 사용한다.
- 기본 화면 이동은 `go()`로 표현한다. 스택에 화면을 추가하거나 반환 결과를 기다리는 요구에는 `push()`를 사용한다.
- 부모·자식 경로를 계층으로 구성해 뒤로 가기와 URL 의미를 일치시킨다.
- URL 단어 구분은 하이픈을 사용한다.
- 호출부에서 원시 경로를 반복하지 않는다. 생성된 라우트 메서드를 우선하고 기존 이름 기반 API에서는 `context.goNamed`·`pushNamed`를 사용한다.
- 딥 링크로 복원할 필수 정보는 경로·쿼리 매개변수로 전달한다. `extra`만으로 복원 가능성을 기대하지 않는다.

## 라우트 구조

권장 계층:

```text
/flutter
  /flutter/news
  /flutter/chat
  /flutter/articles
    /flutter/articles?category=all
    /flutter/articles/article/:id
/android
  /android/news
  /android/chat
```

계층 관계가 사라지는 평면 구조:

```text
/flutter-news
/flutter-chat
/android-news
/android-chat
```

예를 들어 `/flutter/news`의 부모를 `/flutter`로 구성하면 선언된 페이지 계층으로 뒤로 가기를 표현할 수 있다.

## 타입 안전한 정의

`GoRouteData` 클래스와 `@TypedGoRoute` 트리를 정의한다. 경로 문자열은 선언부에만 두고 생성된 메서드로 이동한다. [중첩·셸 라우트](references/typed-routes.md)를 참고한다.

## go와 push

| 메서드 | 의미 | 용도 |
| --- | --- | --- |
| `go()` | 대상 위치에 맞는 페이지 목록으로 전환 | 일반 URL 기반 이동 |
| `push()` | 현재 스택 위에 페이지 추가 | 뒤로 돌아올 화면, 반환 결과 |

```dart
const CategoriesPageRoute(size: 'small', color: 'blue').go(context);
```

```dart
final result = await DialogPageRoute().push<String>(context);
```

브라우저 URL·히스토리 동작은 go_router 버전과 설정에 따라 확인한다. `push()`가 항상 URL을 갱신하지 않는다고 단정하지 않는다.

## BuildContext 확장

```dart
// 권장
context.goNamed('flutterNews');

// 공식 API도 유효하다.
GoRouter.of(context).goNamed('flutterNews');
```

## 매개변수

리소스 식별자는 경로, 선택적 필터·정렬은 쿼리로 표현한다. `extra`는 URL에 포함되지 않으므로 외부 딥 링크가 재구성할 수 없고 복잡한 객체는 직렬화 설정도 필요하다. 필수 식별자를 URL로 넘기고 도착 화면에서 조회한다. [매개변수 예제](references/parameters.md)를 참고한다.

## 리다이렉트와 테스트

전역 인증과 라우트별 권한 리다이렉트를 구분하고 반복 리다이렉트가 없는지 확인한다. [리다이렉트](references/redirects.md), [GoRouter 모킹과 통합 테스트](references/testing.md)를 참고한다.

## 라우트 추가

1. 화면을 만들고 필요하면 Page/View로 나눈다.
2. 타입이 있는 라우트를 적절한 부모 아래 정의한다.
3. `dart run build_runner build --delete-conflicting-outputs`로 코드를 생성한다.
4. 생성된 라우트 클래스로 이동한다.
5. 대상 URL로 앱을 직접 열어 경로·쿼리·뒤로 가기·인증을 검증한다.
