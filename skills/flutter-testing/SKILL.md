---
name: flutter-testing
description: "Dart 단위 테스트, Flutter 위젯·골든 테스트를 작성하거나 검토할 때 사용한다. 테스트 격리, mocktail, pumpApp, 태그와 커버리지를 다룬다."
---

# Dart·Flutter 테스트

프로젝트의 테스트 관례를 확인하고 아래 패턴을 적용한다. Bloc/Cubit 자체 테스트는 [Bloc](../flutter-bloc/SKILL.md), UI 패키지 위젯은 [UI 패키지](../flutter-ui-package/SKILL.md)를 우선 참고한다.

공식 권고와 팀 관례의 구분, SDK·언어 버전, 오류·수명 처리는 [공통 기준](../flutter-review/SKILL.md#공식-기준과-프로젝트-관례)을 적용한다.

## 핵심 기준

- `'works'` 같은 이름 대신 관찰 가능한 동작을 설명한다. 클래스 → 메서드 → 동작 순서의 `group` 계층을 만든다.
- 타입 이름은 `'returns $User'`처럼 보간해 이름 변경이 반영되게 한다.
- 간단한 fake로 동작을 표현할 수 있는지 먼저 검토한다. 호출 스텁·검증에는 기존 모킹 도구를 따르고, 아래 mocktail 예제에서는 파일별 `_MockX`를 쓴다.
- `setUp`·`tearDown`은 필요한 범위에 둔다. main 안의 공통 setup도 유효하며 group 중첩은 격리의 필수 조건이 아니다. 가변 객체는 매 테스트마다 새로 만든다.
- 정적·전역 가변 상태나 파일 간 공유 목으로 순서 의존성을 만들지 않는다.
- 반복 사용하는 테스트 태그는 최상위 const로 정의할 수 있다. 골든 테스트에는 golden 태그를 지정해 선택 실행할 수 있게 한다.
- 위젯 테스트는 동작·콜백·내용·이동을 검증한다. 시각 회귀는 골든으로, 접근성 대상 크기·모션 감소 시간 등 명확한 속성 계약은 직접 assertion으로 검증할 수 있다.
- `test/helpers/pump_app.dart`의 공유 `pumpApp`으로 테마·지역화를 구성한다.
- 연결된 테스트 MCP가 있으면 도구 스키마를 확인하고 사용한다. 없으면 해당 패키지에서 `very_good test`, `flutter test`, `dart test` 중 프로젝트에 맞는 CLI를 실행한다. MCP 전용 훅을 전제하지 않는다.
- 모노레포에서는 반드시 대상 패키지 디렉터리를 지정한다. 도구의 `timeout_seconds`가 있으면 사용하고, CLI의 테스트별 제한과 실행 프로세스 전체 제한은 구분한다. `--help`에 없는 옵션을 추정해서 전달하지 않는다.

## 파일 배치

| 항목 | 규칙 |
| --- | --- |
| 파일 | `_test.dart`로 끝남 |
| 위치 | `test/` 아래 |
| 구조 | `lib/src/models/user.dart` → `test/src/models/user_test.dart` |
| 헬퍼 | `test/helpers/` |

## 그룹과 이름

최상위 그룹에 문자열 대신 타입을 전달하고, 설명을 이어 읽으면 자연스러운 문장이 되게 한다.

```dart
class _MockApiClient extends Mock implements ApiClient {}

void main() {
  group(UserRepository, () {
    late ApiClient apiClient;
    late UserRepository subject;

    setUp(() {
      apiClient = _MockApiClient();
      subject = UserRepository(apiClient: apiClient);
    });

    group('getUser', () {
      test('returns $User when API call succeeds', () async {
        when(() => apiClient.fetchUser(any()))
            .thenAnswer((_) async => User(id: '1', name: 'Dash'));

        final result = await subject.getUser('1');

        expect(result, equals(User(id: '1', name: 'Dash')));
        verify(() => apiClient.fetchUser('1')).called(1);
      });

      test('throws $UserNotFoundException when API returns 404', () {
        when(() => apiClient.fetchUser(any()))
            .thenThrow(ApiException(statusCode: 404));

        expect(
          () => subject.getUser('1'),
          throwsA(isA<UserNotFoundException>()),
        );
      });
    });
  });
}
```

반환값·예외·의존성 호출·방출 상태·조건·경계 사례를 이름에 드러낸다. 예: `'returns $User when API call succeeds'`, `'throws $UserNotFoundException when user is not found'`.

## 격리

각 테스트가 단독·임의 순서·병렬 실행에서 통과해야 한다. 지원되는 러너의 `--test-randomize-ordering-seed random`으로 순서 의존성을 확인한다.

| 문제 | 개선 |
| --- | --- |
| 여러 테스트가 같은 가변 객체 재사용 | 매 테스트 setUp 또는 테스트 본문에서 새로 생성 |
| 최상위 final 목 인스턴스 | late 선언과 setUp 생성 |
| 여러 파일이 가져오는 공개 목 | 파일별 비공개 목 |
| static·global 가변 값 | 제거하거나 매번 초기화 |
| 특정 실행 순서 필요 | 독립적인 준비와 검증 |

비공개 메서드 자체가 아니라 그것을 사용하는 공개 API를 테스트한다.

```dart
// 비공개 _normalizeEmail은 공개 createUser 메서드를 통해 검증한다.
test('normalizes email to lowercase before saving', () async {
  when(() => repository.save(any())).thenAnswer((_) async {});

  await subject.createUser(email: 'Dash@Example.COM');

  final captured = verify(() => repository.save(captureAny())).captured;
  expect(captured.first.email, equals('dash@example.com'));
});
```

## 위젯 테스트

- `testWidgets`를 사용한다. 기본 탐색은 `find.byType`, 사용자에게 보이는 문구는 `find.text`, 모호한 경우에만 키를 쓴다.
- 렌더링·이동·호출·갱신 같은 동작별로 그룹을 나눈다.
- 격리하려는 경계에 따라 fake·`MockBloc`·`MockCubit` 또는 실제 Bloc을 주입한다. 실제 Bloc을 사용해도 `testWidgets`에서 실행하면 위젯 테스트이며, 기기에서 앱 전체를 검증하는 integration_test와 구분한다.
- 유한한 프레임 진행에는 `pump()`를 우선한다. 반복 애니메이션에는 `pumpAndSettle()`을 쓰지 않는다.

공통 앱 구성을 헬퍼에 둔다.

```dart
// test/helpers/pump_app.dart
extension PumpApp on WidgetTester {
  Future<void> pumpApp(Widget widget) {
    return pumpWidget(MaterialApp(home: widget));
  }
}
```

공통 내보내기 파일을 사용한다.

```dart
import '../helpers/helpers.dart';

void main() {
  group(MyWidget, () {
    testWidgets('renders greeting text', (tester) async {
      await tester.pumpApp(const MyWidget());

      expect(find.text('Hello'), findsOneWidget);
    });
  });
}
```

탭·입력 뒤에 프레임을 진행시키고 검증한다. 내부 구현 세부사항의 무의미한 고정은 피하되 명시된 크기·테마·접근성 계약은 직접 검증한다.

## 참고 문서

- [Mocktail](references/mocktail.md): 목, 스텁, 인수 검증
- [수명과 테스트 패턴](references/test-patterns.md): 비동기·스트림·예외·콜백
- [위젯](references/widget-tests.md): Bloc, 테마, 지역화, 탐색
- [골든](references/golden-tests.md): 태그, 기준 이미지 갱신
- [매처](references/matchers.md)
- [설정과 실행](references/configuration.md)
- [커버리지](references/coverage.md)
- [애니메이션](references/animation-testing.md)
