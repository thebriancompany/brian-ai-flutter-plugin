# 자주 사용하는 패턴

## Bloc으로 기능 추가

1. `lib/<feature>/` 디렉터리와 `<feature>.dart` 내보내기 파일을 만든다.
2. `bloc/<feature>_event.dart`에 sealed 이벤트와 하위 클래스를 정의한다.
3. `bloc/<feature>_state.dart`에 Equatable 기반 상태를 정의한다.
4. `bloc/<feature>_bloc.dart`에 저장소를 주입하고 이벤트 핸들러를 등록한다.
5. `view/<feature>_page.dart`에서 `BlocProvider`를 제공한다.
6. `view/<feature>_view.dart`에서 `BlocBuilder`로 상태를 소비한다.
7. `test/<feature>/`에 같은 구조를 만들고 모든 이벤트 핸들러와 상태 전이를 `blocTest`로 검증한다.

## Cubit으로 기능 추가

1. `lib/<feature>/`와 `<feature>.dart`를 만든다.
2. `cubit/<feature>_state.dart`에 상태를 정의한다.
3. `cubit/<feature>_cubit.dart`에 `emit`을 호출하는 공개 메서드를 구현한다.
4. `BlocProvider`·`BlocBuilder`를 사용하는 Page와 View를 만든다.
5. 동일한 `test/<feature>/` 구조에 공개 메서드별 `blocTest`를 작성한다.

## 비동기 작업

```dart
Future<void> _onDataRequested(
  DataRequested event,
  Emitter<DataState> emit,
) async {
  emit(state.copyWith(status: DataStatus.loading));
  try {
    final data = await _repository.fetchData();
    emit(state.copyWith(status: DataStatus.success, data: data));
  } on Exception catch (error, stackTrace) {
    addError(error, stackTrace);
    emit(state.copyWith(status: DataStatus.failure, error: 'load_failed'));
  }
}
```

`addError`의 관찰자·로그는 민감 정보를 제거한다. 상태에는 안정적인 오류 코드만 넣고 화면에서 지역화한다. 예상 밖 프로그래밍 오류를 일반 실패 상태로 삼키지 않는다.

## 이벤트 변환기

`package:bloc_concurrency`로 처리 방식을 제어한다.

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';

class SearchBloc extends Bloc<SearchEvent, SearchState> {
  SearchBloc({required SearchRepository repository})
    : _repository = repository,
      super(const SearchState()) {
    on<SearchTermChanged>(
      _onSearchTermChanged,
      transformer: restartable(), // 이전 핸들러의 방출을 취소한다. HTTP 요청 자체는 별도 취소가 필요하다.
    );
  }
}
```

| 변환기 | 동작 |
| --- | --- |
| `concurrent()` | 모든 이벤트를 동시에 처리하며 기본 동작에 해당 |
| `sequential()` | 하나씩 순서대로 처리 |
| `droppable()` | 처리 중 들어오는 새 이벤트 무시 |
| `restartable()` | 현재 처리를 취소하고 최신 이벤트 처리 |

변환기는 같은 `on<Event>` 등록의 이벤트에 적용된다. 서로 다른 이벤트 타입 전체를 직렬화하지 않는다. `restartable`도 외부 Future·서버 쓰기를 되돌리지 않으며 비동기 완료 후 `emit.isDone`을 확인한다.

## 단일 상태 클래스

데이터 형태가 같으면 상태 열거형과 하나의 클래스를 사용한다. `final`만으로 List 내용은 불변이 되지 않아 복사해 보관하며 Todo 자체도 불변이어야 한다. `copyWith(clearError: true)`는 이전 오류를 지운다. 컬렉션을 동결하므로 이 예제의 생성자는 const가 아니다.

| 필드 | 타입 | 용도 |
| --- | --- | --- |
| `status` | `enum` | 현재 로딩 상태 |
| `items` | `List<Item>` | 읽어 온 데이터 |
| `error` | `String?` | 실패 메시지 |

```dart
enum TodoListStatus { initial, loading, success, failure }

class TodoListState extends Equatable {
  TodoListState({
    this.status = TodoListStatus.initial,
    List<Todo> todos = const [],
    this.error,
  }) : todos = List.unmodifiable(todos);

  final TodoListStatus status;
  final List<Todo> todos;
  final String? error;
  TodoListState copyWith({
    TodoListStatus? status,
    List<Todo>? todos,
    String? error,
    bool clearError = false,
  }) {
    return TodoListState(
      status: status ?? this.status,
      todos: todos ?? this.todos,
      error: clearError ? null : (error ?? this.error),
    );
  }

  @override
  List<Object?> get props => [status, todos, error];
}
```
