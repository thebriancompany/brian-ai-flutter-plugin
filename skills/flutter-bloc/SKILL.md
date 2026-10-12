---
name: flutter-bloc
description: "Flutter/Dart Bloc·Cubit의 구현과 테스트를 작성하거나 검토할 때 사용한다. 이벤트·상태 설계, Page/View 분리, blocTest와 mocktail을 다룬다."
---

# Bloc 상태 관리

BLoC 패턴으로 비즈니스 로직과 화면 계층을 분리한다. 기존 프로젝트와 사용자의 명시적 선택을 우선하고 다음 기준을 적용한다.

## 핵심 기준

- Bloc/Cubit 테스트는 `package:bloc_test`의 `blocTest()`로 작성한다. 일반 `test()`와 수동 스트림 검증으로 대체하지 않는다.
- 모킹은 `package:mocktail`을 사용한다.
- `build:` 콜백에서 매번 새로운 Bloc/Cubit을 만든다. `setUp`에서 만든 인스턴스를 여러 테스트가 공유하지 않게 하고 수명 관리는 `blocTest`에 맡긴다.
- Bloc끼리 직접 의존하지 않는다. UI 또는 공유 저장소를 통해 통신한다.
- Page는 `BlocProvider`로 인스턴스를 제공하고 View는 `BlocBuilder`·`BlocListener`로 소비한다.
- 이벤트와 여러 상태 타입은 `sealed` 계층으로 표현해 Dart 3 `switch`의 완전성 검사를 활용한다.
- 상태와 이벤트는 `Equatable`을 상속하고 `props`를 재정의해 값 동등성을 제공한다.
- 비즈니스 로직은 위젯이 아니라 Bloc/Cubit에 둔다. 하나의 기능 관심사에 하나의 Bloc/Cubit을 둔다.
- `emit`은 해당 `on<Event>` 핸들러 또는 Cubit 메서드의 수명 안에서만 호출한다. 핸들러보다 오래 살아 있는 구독·콜백에서 호출하지 않는다.
- Dart 3.13 이상을 사용하는 프로젝트에서는 기본 생성자의 선언 매개변수(`class const ProfileRequested(final String userId) extends ProfileEvent`)를 활용한다. 낮은 SDK 버전에서는 기존 생성자 문법을 유지한다.

## Cubit과 Bloc 선택

| 항목 | Cubit | Bloc |
| --- | --- | --- |
| API | 함수 → `emit(state)` | 이벤트 → `on<Event>` → `emit(state)` |
| 복잡도 | 낮음 | 상대적으로 높음 |
| 추적 | 이벤트 로그 없음 | 이벤트와 전이 추적 |
| 용도 | 단순 상태, UI 중심 로직 | 복잡한 흐름, 이벤트 변환 |
| 테스트 | 메서드 호출 후 상태 검증 | 이벤트 추가 후 상태 검증 |

### Cubit 예제

```dart
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
}
```

### Bloc 예제

```dart
sealed class CounterEvent extends Equatable {
  const CounterEvent();

  @override
  List<Object> get props => [];
}

final class CounterIncrementPressed extends CounterEvent {}
final class CounterDecrementPressed extends CounterEvent {}

class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<CounterIncrementPressed>((event, emit) => emit(state + 1));
    on<CounterDecrementPressed>((event, emit) => emit(state - 1));
  }
}
```

## 이름 규칙

이벤트는 `BlocSubject` + `Noun` + `VerbPastTense` 형식으로 쓴다.

| 이벤트 | 의미 |
| --- | --- |
| `TodoListSubscriptionRequested` | 할 일 목록 스트림 구독 요청 |
| `TodoListTodoDeleted` | 특정 할 일 삭제 |
| `TodoListUndoDeletionRequested` | 마지막 삭제 취소 요청 |
| `LoginFormSubmitted` | 로그인 폼 제출 |
| `ProfilePageRefreshed` | 프로필 화면 새로 고침 |

```dart
sealed class TodoListEvent extends Equatable {
  const TodoListEvent();

  @override
  List<Object> get props => [];
}

final class TodoListSubscriptionRequested extends TodoListEvent {}

final class const TodoListTodoDeleted({required final Todo todo})
    extends TodoListEvent {
  @override
  List<Object> get props => [todo];
}
```

상태마다 데이터가 다르면 하위 클래스로 나눈다.

| 상태 | 의미 |
| --- | --- |
| `LoginInitial` | 초기 상태 |
| `LoginInProgress` | 로그인 요청 중 |
| `LoginSuccess` | 로그인 성공 |
| `LoginFailure` | 로그인 실패 |

```dart
sealed class LoginState extends Equatable {
  const LoginState();

  @override
  List<Object> get props => [];
}

final class LoginInitial extends LoginState {}
final class LoginInProgress extends LoginState {}
final class const LoginSuccess({required final User user}) extends LoginState {
  @override
  List<Object> get props => [user];
}
final class const LoginFailure({required final String error})
    extends LoginState {
  @override
  List<Object> get props => [error];
}
```

모든 상태의 데이터 형태가 같다면 `status` 열거형과 데이터 필드, `copyWith`를 갖는 단일 클래스를 사용한다. [상태 패턴](references/patterns.md)을 참고한다.

## 계층 구조

| 계층 | 구성 | 의존 대상 |
| --- | --- | --- |
| 화면 | Page, View, Widget | 비즈니스 로직 |
| 비즈니스 로직 | Bloc, Cubit | 데이터 계층 |
| 데이터 | Repository, Data Provider | 외부 데이터 원천 |

Repository는 데이터 원천을 추상화하고 Bloc/Cubit에 명확한 API를 제공한다. 테스트 디렉터리는 기능 폴더 구조를 따른다. [구조 예제](references/architecture.md)를 참고한다.

## Flutter 위젯

`BlocProvider`로 하위 트리에 상태 관리 객체를 제공한다. 상태의 일부만 리빌드 조건이면 `BlocSelector`, 이동·스낵바 같은 부수 효과에는 `BlocListener`를 사용한다. 함께 필요하면 `BlocConsumer`를 사용한다.

콜백에서는 `context.read`, `build`에서는 `context.watch` 또는 `BlocBuilder`를 사용한다. `build` 밖에서 `context.watch`를 호출하지 않는다.

## 필요한 참고 문서

- [계층과 폴더](references/architecture.md): Repository와 테스트 배치
- [위젯](references/widgets.md): Page/View, 컨텍스트 확장, 리스너
- [테스트](references/testing.md): `blocTest`, 의존성 모킹, 위젯 통합
- [상태와 이벤트 패턴](references/patterns.md): 새 기능, 비동기 처리, 이벤트 변환
