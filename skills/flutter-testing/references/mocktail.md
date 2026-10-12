# Mocktail 모킹

`package:mocktail`은 코드 생성과 build_runner 없이 사용한다.

## 목 생성

사용하는 파일 안에서 비공개 클래스로 선언한다.

```dart
class _MockUserRepository extends Mock implements UserRepository {}

class _MockAnalyticsClient extends Mock implements AnalyticsClient {}

class _FakeUser extends Fake implements User {}
```

미구현 메서드가 null 대신 오류를 내는 구체적 대역이 필요하면 `Fake`를 쓴다.

## 스텁

| 메서드 | 용도 |
| --- | --- |
| `thenReturn` | 동기 반환값 |
| `thenAnswer` | Future·Stream 등 응답 |
| `thenThrow` | 예외 발생 |

스트림 예제:

```dart
when(() => mock.updates).thenAnswer((_) => Stream.fromIterable([1, 2, 3]));
```

## 인수 매처

| 매처 | 용도 |
| --- | --- |
| `any()` | 임의 값, 사용자 정의 타입의 fallback 등록 필요 |
| `any(that: matcher)` | 조건을 만족하는 값 |
| `captureAny()` | 이후 검증할 인수 캡처 |

```dart
test('passes the correct user to the repository', () async {
  when(() => repository.save(any())).thenAnswer((_) async {});

  await subject.createUser(name: 'Dash');

  final captured = verify(() => repository.save(captureAny())).captured;
  expect(captured.first, isA<User>().having((u) => u.name, 'name', 'Dash'));
});
```

## 호출 검증

| 메서드 | 용도 |
| --- | --- |
| `verify(() => mock.method()).called(n)` | 정확한 횟수 |
| `verifyNever(() => mock.method())` | 호출 없음 |
| `verifyNoMoreInteractions(mock)` | 다른 호출 없음 |
| `verifyInOrder([...])` | 호출 순서 |

## Fallback 값

`any()`·`captureAny()`가 쓰는 사용자 정의 타입은 그룹의 `setUpAll`에서 한 번 등록한다.

```dart
group(OrderRepository, () {
  late ApiClient apiClient;

  setUpAll(() {
    registerFallbackValue(Order(id: '', items: const []));
    registerFallbackValue(Uri.parse('https://example.com'));
  });

  setUp(() {
    apiClient = _MockApiClient();
  });

  // 테스트 추가
});
```

Fallback은 매처 인수의 타입 안전한 자리표시자다. 스텁이 없는 호출의 반환값으로 사용되는 것이 아니다. 해당 용도에서는 필드의 구체적인 값이 중요하지 않다.
