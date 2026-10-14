# 수명과 공통 패턴

| 메서드 | 실행 시점 | 용도 |
| --- | --- | --- |
| `setUp` | 각 테스트 전 | 새 목과 대상 생성 |
| `tearDown` | 각 테스트 후 | 스트림·컨트롤러 정리 |
| `setUpAll` | 그룹 전체 전 한 번 | fallback·공유 초기화 |
| `tearDownAll` | 그룹 전체 후 한 번 | 공유 자원 해제 |

테스트에 필요한 범위의 main 또는 group 안에 둔다. 등록 위치보다 각 테스트의 격리와 자원 정리가 중요하다.

## 비동기 메서드

```dart
test('returns list of users from API', () async {
  when(() => apiClient.fetchUsers())
      .thenAnswer((_) async => [User(id: '1', name: 'Dash')]);

  final result = await subject.getUsers();

  expect(result, hasLength(1));
  expect(result.first.name, equals('Dash'));
});
```

## 스트림

```dart
test('emits updated values when data changes', () {
  when(() => repository.watch())
      .thenAnswer((_) => Stream.fromIterable([1, 2, 3]));

  expect(
    subject.valueStream,
    emitsInOrder([1, 2, 3]),
  );
});
```

## 예외

```dart
test('throws $FormatException when input is invalid', () {
  expect(
    () => subject.parse('invalid'),
    throwsA(
      isA<FormatException>().having(
        (e) => e.message,
        'message',
        contains('invalid'),
      ),
    ),
  );
});
```

## Equatable

값을 `equals`로 직접 비교한다.

```dart
test('returns expected $User', () async {
  when(() => apiClient.fetchUser('1'))
      .thenAnswer((_) async => User(id: '1', name: 'Dash'));

  final result = await subject.getUser('1');

  expect(result, equals(User(id: '1', name: 'Dash')));
});
```

## 콜백

```dart
test('calls onSuccess callback when operation completes', () async {
  var callbackCalled = false;
  when(() => repository.save(any())).thenAnswer((_) async {});

  await subject.save(
    data: 'test',
    onSuccess: () => callbackCalled = true,
  );

  expect(callbackCalled, isTrue);
});
```
