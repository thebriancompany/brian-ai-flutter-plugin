# Bloc/Cubit 테스트

## `blocTest()` 매개변수

| 매개변수 | 타입 | 용도 |
| --- | --- | --- |
| `build` | `() => Bloc/Cubit` | 테스트 대상 생성 |
| `act` | `(bloc) => void` | 대상에 동작 수행 |
| `expect` | `() => List<State>` | 순서대로 방출할 상태 |
| `seed` | `() => State` | `act` 전 초기 상태 |
| `setUp` | `() => void` | `build` 전에 실행 |
| `verify` | `(bloc) => void` | `expect` 이후 추가 검증 |
| `errors` | `() => List<Matcher>` | 예상 오류 |
| `wait` | `Duration` | 디바운스 등 검증 전 대기 |

## Cubit 예제

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:my_app/counter/counter.dart';

void main() {
  group('CounterCubit', () {
    test('initial state is 0', () {
      final cubit = CounterCubit();
      addTearDown(cubit.close);
      expect(cubit.state, equals(0));
    });

    blocTest<CounterCubit, int>(
      'emits [1] when increment is called',
      build: CounterCubit.new,
      act: (cubit) => cubit.increment(),
      expect: () => [1],
    );

    blocTest<CounterCubit, int>(
      'emits [2] when increment is called from 1',
      build: CounterCubit.new,
      seed: () => 1,
      act: (cubit) => cubit.increment(),
      expect: () => [2],
    );
  });
}
```

## Bloc 예제

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:my_app/todos/todos.dart';

class MockTodoRepository extends Mock implements TodoRepository {}

void main() {
  late TodoRepository todoRepository;

  setUp(() {
    todoRepository = MockTodoRepository();
  });

  group('TodosBloc', () {
    blocTest<TodosBloc, TodosState>(
      'emits [loading, success] when subscription is requested',
      setUp: () {
        when(() => todoRepository.getTodos())
            .thenAnswer((_) async => [Todo(id: '1', title: 'Test')]);
      },
      build: () => TodosBloc(todoRepository: todoRepository),
      act: (bloc) => bloc.add(const TodosSubscriptionRequested()),
      expect: () => [
        const TodosState(status: TodosStatus.loading),
        isA<TodosState>()
            .having((s) => s.status, 'status', TodosStatus.success)
            .having((s) => s.todos, 'todos', hasLength(1)),
      ],
      verify: (_) {
        verify(() => todoRepository.getTodos()).called(1);
      },
    );

    blocTest<TodosBloc, TodosState>(
      'emits [loading, failure] when repository throws',
      setUp: () {
        when(() => todoRepository.getTodos()).thenThrow(Exception('oops'));
      },
      build: () => TodosBloc(todoRepository: todoRepository),
      act: (bloc) => bloc.add(const TodosSubscriptionRequested()),
      expect: () => [
        const TodosState(status: TodosStatus.loading),
        isA<TodosState>().having(
          (s) => s.status,
          'status',
          TodosStatus.failure,
        ),
      ],
    );
  });
}
```

## 의존성 모킹

```dart
import 'package:mocktail/mocktail.dart';

// 목 생성
class MockTodoRepository extends Mock implements TodoRepository {}

// 메서드 스텁
when(() => repository.getTodos()).thenAnswer((_) async => []);
when(() => repository.addTodo(any())).thenAnswer((_) async {});

// 호출 검증
verify(() => repository.getTodos()).called(1);
verifyNever(() => repository.deleteTodo(any()));

// 사용자 정의 타입의 fallback 등록
setUpAll(() {
  registerFallbackValue(Todo(id: '', title: ''));
});
```

## 위젯 통합 테스트

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:my_app/todos/todos.dart';

class MockTodosBloc extends MockBloc<TodosEvent, TodosState>
    implements TodosBloc {}

void main() {
  late TodosBloc todosBloc;

  setUp(() {
    todosBloc = MockTodosBloc();
  });

  group('TodosView', () {
    testWidgets('renders loading indicator when status is loading', (
      tester,
    ) async {
      when(() => todosBloc.state)
          .thenReturn(const TodosState(status: TodosStatus.loading));

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(value: todosBloc, child: const TodosView()),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('renders todos when status is success', (tester) async {
      final todos = [Todo(id: '1', title: 'Test Todo')];
      when(() => todosBloc.state)
          .thenReturn(TodosState(status: TodosStatus.success, todos: todos));

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(value: todosBloc, child: const TodosView()),
        ),
      );

      expect(find.text('Test Todo'), findsOneWidget);
    });
  });
}
```
