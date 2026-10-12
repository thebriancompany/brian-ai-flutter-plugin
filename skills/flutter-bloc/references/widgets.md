# Flutter 위젯

| 위젯 | 용도 |
| --- | --- |
| `BlocProvider` | Bloc/Cubit을 생성해 하위 트리에 제공 |
| `BlocBuilder` | 상태 변경 시 위젯 재빌드 |
| `BlocListener` | 이동·스낵바 같은 부수 효과 실행 |
| `BlocConsumer` | Builder와 Listener 결합 |
| `BlocSelector` | 선택한 속성이 바뀔 때만 재빌드 |
| `MultiBlocProvider` | 중첩 없이 여러 Bloc/Cubit 제공 |
| `MultiBlocListener` | 중첩 없이 여러 리스너 등록 |
| `RepositoryProvider` | 하위 트리에 Repository 제공 |

## 컨텍스트 확장

| 확장 | 용도 | 재빌드 |
| --- | --- | --- |
| `context.read<T>()` | 인스턴스 한 번 읽기 | 없음 |
| `context.watch<T>()` | 인스턴스 접근과 변경 구독 | 있음 |
| `context.select<T, R>()` | 상태의 특정 속성 구독 | 선택적으로 발생 |

- `onPressed`, `onTap`, `initState`에서는 `context.read`를 사용한다.
- `build`에서는 `context.watch` 또는 `BlocBuilder`를 사용한다.
- `build` 밖에서는 `context.watch`를 사용하지 않는다.

## Page/View 패턴

```dart
class TodosPage extends StatelessWidget {
  const TodosPage({super.key});

  static Route<void> route() {
    return MaterialPageRoute(builder: (_) => const TodosPage());
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => TodosBloc(
        todoRepository: context.read<TodoRepository>(),
      )..add(const TodosSubscriptionRequested()),
      child: const TodosView(),
    );
  }
}

class TodosView extends StatelessWidget {
  const TodosView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Todos')),
      body: BlocBuilder<TodosBloc, TodosState>(
        builder: (context, state) {
          return switch (state.status) {
            TodosStatus.initial || TodosStatus.loading =>
              const Center(child: CircularProgressIndicator()),
            TodosStatus.success =>
              ListView.builder(
                itemCount: state.todos.length,
                itemBuilder: (context, index) =>
                    TodoListTile(todo: state.todos[index]),
              ),
            TodosStatus.failure =>
              Center(child: Text('Error: ${state.error}')),
          };
        },
      ),
    );
  }
}
```

## 부수 효과를 위한 BlocListener

```dart
BlocListener<LoginBloc, LoginState>(
  listener: (context, state) {
    if (state is LoginFailure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.error)),
      );
    }
    if (state is LoginSuccess) {
      Navigator.of(context).pushReplacement(HomePage.route());
    }
  },
  child: const LoginForm(),
)
```
