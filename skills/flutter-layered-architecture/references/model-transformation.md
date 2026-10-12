# 모델 변환

## 데이터 모델과 도메인 모델

외부 API 형태와 내부 앱 표현을 구분하고 저장소에서 변환한다.

```text
API JSON → UserResponse(데이터 모델) → User(도메인 모델)
```

## 이름 있는 팩토리 생성자

도메인 모델에 응답을 변환하는 팩토리를 둘 수 있다.

```dart
import 'package:equatable/equatable.dart';
import 'package:user_api_client/user_api_client.dart' show UserResponse;

class const User({
  required final String id,
  required final String email,
  required final String displayName,
  final String? avatarUrl,
}) extends Equatable {
  /// [UserResponse]에서 [User]를 생성한다.
  factory User.fromResponse(UserResponse response) {
    return User(
      id: response.id,
      email: response.email,
      displayName: response.displayName,
      avatarUrl: response.avatarUrl,
    );
  }

  @override
  List<Object?> get props => [id, email, displayName, avatarUrl];
}
```

저장소에서 사용한다.

```dart
Future<User> getUser(String userId) async {
  final response = await _userApiClient.getUser(userId);
  return User.fromResponse(response);
}
```

## null 허용 필드

선택적이거나 형태가 달라질 수 있는 필드를 처리한다.

```dart
factory User.fromResponse(UserResponse response) {
  return User(
    id: response.id,
    email: response.email,
    // API 필드가 없을 때의 기본값
    displayName: response.displayName ?? 'Unknown',
    // null 허용 필드는 그대로 전달한다.
    avatarUrl: response.avatarUrl,
  );
}
```

## 여러 원천 결합

하나의 도메인 모델에 여러 클라이언트의 정보가 필요할 때:

```dart
class UserRepository {
  const UserRepository({
    required UserApiClient userApiClient,
    required LocalStorageClient localStorageClient,
  })  : _userApiClient = userApiClient,
        _localStorageClient = localStorageClient;

  final UserApiClient _userApiClient;
  final LocalStorageClient _localStorageClient;

  Future<User> getUser(String userId) async {
    final response = await _userApiClient.getUser(userId);
    final cachedNickname = _localStorageClient.read('nickname_$userId');

    return User(
      id: response.id,
      email: response.email,
      displayName: cachedNickname ?? response.displayName,
      avatarUrl: response.avatarUrl,
    );
  }
}
```

## 변환 테스트

```dart
group('User.fromResponse', () {
  test('transforms $UserResponse to $User', () {
    const response = UserResponse(
      id: '1',
      email: 'dash@example.com',
      displayName: 'Dash',
      avatarUrl: 'https://example.com/avatar.png',
    );

    expect(
      User.fromResponse(response),
      equals(
        const User(
          id: '1',
          email: 'dash@example.com',
          displayName: 'Dash',
          avatarUrl: 'https://example.com/avatar.png',
        ),
      ),
    );
  });

  test('handles null avatarUrl', () {
    const response = UserResponse(
      id: '1',
      email: 'dash@example.com',
      displayName: 'Dash',
    );

    expect(User.fromResponse(response).avatarUrl, isNull);
  });
});
```
