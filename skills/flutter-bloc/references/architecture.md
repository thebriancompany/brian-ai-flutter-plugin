# 계층 구조

## 데이터 계층

Repository는 데이터 원천을 추상화하고 Bloc/Cubit에 명확한 API를 제공한다.

```dart
class TodoRepository {
  const TodoRepository({required TodoApiClient apiClient})
      : _apiClient = apiClient;

  final TodoApiClient _apiClient;

  Future<List<Todo>> getTodos() => _apiClient.fetchTodos();

  Future<void> addTodo(Todo todo) => _apiClient.createTodo(todo);

  Future<void> deleteTodo(String id) => _apiClient.deleteTodo(id);
}
```

## 기능별 폴더 구조

```text
lib/
├── todos/
│   ├── todos.dart                  # 공개 API 배럴
│   ├── bloc/
│   │   ├── todos_bloc.dart
│   │   ├── todos_event.dart
│   │   └── todos_state.dart
│   ├── view/
│   │   ├── todos_page.dart         # BlocProvider로 Bloc 제공
│   │   └── todos_view.dart         # BlocBuilder로 상태 소비
│   └── widgets/
│       └── todo_list_tile.dart
test/
├── todos/
│   ├── bloc/
│   │   └── todos_bloc_test.dart
│   ├── view/
│   │   ├── todos_page_test.dart
│   │   └── todos_view_test.dart
│   └── widgets/
│       └── todo_list_tile_test.dart
```
