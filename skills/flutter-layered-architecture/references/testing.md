# 패키지별 테스트

## 데이터 클라이언트

HTTP 클라이언트를 모킹하고 요청·응답을 확인한다.

```dart
import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:mocktail/mocktail.dart';
import 'package:test/test.dart';
import 'package:user_api_client/user_api_client.dart';

class _MockHttpClient extends Mock implements http.Client {}

void main() {
  group(UserApiClient, () {
    late http.Client httpClient;
    late UserApiClient subject;

    setUpAll(() {
      registerFallbackValue(Uri.parse('https://example.com'));
    });

    setUp(() {
      httpClient = _MockHttpClient();
      subject = UserApiClient(
        baseUrl: 'https://api.test.com',
        httpClient: httpClient,
      );
    });

    group('getUser', () {
      test('returns $UserResponse when status is 200', () async {
        when(() => httpClient.get(any())).thenAnswer(
          (_) async => http.Response(
            json.encode({
              'id': '1',
              'email': 'dash@example.com',
              'display_name': 'Dash',
              'avatar_url': null,
            }),
            200,
          ),
        );

        final result = await subject.getUser('1');

        expect(
          result,
          isA<UserResponse>()
              .having((r) => r.id, 'id', '1')
              .having((r) => r.email, 'email', 'dash@example.com')
              .having((r) => r.displayName, 'displayName', 'Dash'),
        );

        verify(() => httpClient.get(Uri.parse('https://api.test.com/users/1')))
            .called(1);
      });

      test('throws $UserApiException when status is not 200', () {
        when(() => httpClient.get(any()))
            .thenAnswer((_) async => http.Response('Not found', 404));

        expect(
          () => subject.getUser('1'),
          throwsA(
            isA<UserApiException>().having(
              (e) => e.statusCode,
              'statusCode',
              404,
            ),
          ),
        );
      });
    });
  });
}
```

## 저장소

데이터 클라이언트를 모킹하고 도메인 변환을 확인한다.

```dart
import 'package:mocktail/mocktail.dart';
import 'package:test/test.dart';
import 'package:user_api_client/user_api_client.dart';
import 'package:user_repository/user_repository.dart';

class _MockUserApiClient extends Mock implements UserApiClient {}

void main() {
  group(UserRepository, () {
    late UserApiClient userApiClient;
    late UserRepository subject;

    setUp(() {
      userApiClient = _MockUserApiClient();
      subject = UserRepository(userApiClient: userApiClient);
    });

    group('getUser', () {
      const userId = '1';
      final userResponse = UserResponse(
        id: userId,
        email: 'dash@example.com',
        displayName: 'Dash',
      );

      test('returns $User when API call succeeds', () async {
        when(() => userApiClient.getUser(userId))
            .thenAnswer((_) async => userResponse);

        final result = await subject.getUser(userId);

        expect(
          result,
          equals(
            const User(
              id: userId,
              email: 'dash@example.com',
              displayName: 'Dash',
            ),
          ),
        );
      });

      test('throws $UserNotFoundException when API returns 404', () {
        when(() => userApiClient.getUser(userId))
            .thenThrow(const UserApiException(404, 'Not found'));

        expect(
          () => subject.getUser(userId),
          throwsA(isA<UserNotFoundException>()),
        );
      });

      test('throws $UserLoadException for non-404 errors', () {
        when(() => userApiClient.getUser(userId))
            .thenThrow(const UserApiException(500, 'Server error'));

        expect(
          () => subject.getUser(userId),
          throwsA(
            isA<UserLoadException>().having(
              (e) => e.statusCode,
              'statusCode',
              500,
            ),
          ),
        );
      });
    });
  });
}
```

## 모노레포 전체 실행

대상 앱 루트에서 지원되는 `very_good test --recursive --coverage --min-coverage <프로젝트-목표>`을 사용할 수 있다. 실제 옵션은 `--help`로 확인한다. MCP에서는 셸 옵션 문자열을 넘기지 말고 스키마의 `recursive`, `coverage`, `min_coverage`, `directory` 필드를 사용한다. 모든 하위 패키지 결과를 확인한다.

## 기준

- 각 계층은 직접 의존성만 모킹한다. 저장소 테스트에서 HTTP까지 두 단계 내려가지 않는다.
- 모델의 모든 필드·null·경계값 변환을 검증한다.
- 테스트 폴더는 lib 구조를 따른다.
- 실제 네트워크로 계층 단위 테스트를 불안정하게 만들지 않는다.
- 그룹마다 `late`·`setUp`으로 새 인스턴스를 생성해 가변 상태를 공유하지 않는다.
