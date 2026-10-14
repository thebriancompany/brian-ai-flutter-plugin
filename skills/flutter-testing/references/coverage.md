# 커버리지

## 누락 경로 보완

공개 메서드의 경계값·오류·빈 입력, if/else·switch·조기 반환, catch와 오류 상태를 검증한다. `copyWith`의 각 필드, Equatable의 동등성·hashCode, 재정의한 `toString`도 실제 계약에 맞춰 확인한다. 구현을 그대로 반복하는 무의미한 검증으로 숫자만 채우지 않는다.

## copyWith 예제

```dart
group('copyWith', () {
  test('returns equal state when no arguments are provided', () {
    final state = TodoListState(
      status: TodoListStatus.success,
      todos: [Todo(id: '1', title: 'Test')],
    );

    expect(state.copyWith(), equals(state));
  });

  test('returns updated status when status is provided', () {
    final state = TodoListState();

    final result = state.copyWith(status: TodoListStatus.loading);

    expect(result.status, equals(TodoListStatus.loading));
    expect(result.todos, equals(state.todos));
  });

  test('returns updated todos when todos is provided', () {
    final state = TodoListState();
    final todos = [Todo(id: '1', title: 'New')];

    final result = state.copyWith(todos: todos);

    expect(result.todos, equals(todos));
    expect(result.status, equals(state.status));
  });
});
```

## 패키지

| 패키지 | 용도 | 개발 의존성 |
| --- | --- | --- |
| `test` | Dart 테스트 | 예 |
| `flutter_test` | Flutter 테스트와 test 재노출 | 예, SDK |
| `mocktail` | 목과 스텁 | 예 |
| `fake_async` | 타이머·마이크로태스크 제어 | 예 |
| `clock` | 시간 의존 로직에 시계 주입 | 아니오 |
| `bloc_test` | Bloc/Cubit 테스트와 목 | 예 |

## 가져오기

| import | 용도 |
| --- | --- |
| `package:test/test.dart` | 순수 Dart |
| `package:flutter_test/flutter_test.dart` | Flutter |
| `package:mocktail/mocktail.dart` | Mock·Fake·when·verify |
| `../helpers/helpers.dart` | 위젯·골든 테스트의 pumpApp·태그 상수 |
