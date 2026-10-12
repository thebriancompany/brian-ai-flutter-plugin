# 사용자 프로필 전체 예제

네 계층을 연결한 코드다. 예제의 의존성 버전과 Dart 문법은 대상 프로젝트 SDK에 맞게 조정한다.

## 데이터 계층: user_api_client

`packages/user_api_client/pubspec.yaml`

```yaml
name: user_api_client
description: HTTP client for the User API.
version: 0.1.0+1
publish_to: none

environment:
  sdk: ^3.11.0

dependencies:
  http: ^1.4.0
  json_annotation: ^4.9.0

dev_dependencies:
  build_runner: ^2.4.0
  json_serializable: ^6.9.0
  mocktail: ^1.0.0
  test: ^1.25.0
  very_good_analysis: ^7.0.0
```

`packages/user_api_client/lib/user_api_client.dart`

```dart
/// 사용자 API용 HTTP 클라이언트.
library;

export 'src/models/models.dart';
export 'src/user_api_client.dart';
```

`packages/user_api_client/lib/src/models/models.dart`

```dart
export 'user_response.dart';
```

`packages/user_api_client/lib/src/models/user_response.dart`

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user_response.g.dart';

@JsonSerializable()
class const UserResponse({
  required final String id,
  required final String email,
  @JsonKey(name: 'display_name') required final String displayName,
  @JsonKey(name: 'avatar_url') final String? avatarUrl,
}) {
  factory UserResponse.fromJson(Map<String, dynamic> json) =>
      _$UserResponseFromJson(json);

  Map<String, dynamic> toJson() => _$UserResponseToJson(this);
}
```

`packages/user_api_client/lib/src/user_api_client.dart`

```dart
import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:user_api_client/user_api_client.dart';

/// 사용자 API 요청 실패 예외.
class const UserApiException(final int statusCode, final String message)
    implements Exception;

/// 사용자 API용 HTTP 클라이언트.
class UserApiClient {
  UserApiClient({
    required String baseUrl,
    http.Client? httpClient,
  })  : _baseUrl = baseUrl,
        _httpClient = httpClient ?? http.Client();

  final String _baseUrl;
  final http.Client _httpClient;

  /// 지정한 [userId]의 사용자를 조회한다.
  Future<UserResponse> getUser(String userId) async {
    final response = await _httpClient.get(
      Uri.parse('$_baseUrl/users/$userId'),
    );

    if (response.statusCode != 200) {
      throw UserApiException(response.statusCode, response.body);
    }

    return UserResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }
}
```

## 데이터 계층: local_storage_client

`packages/local_storage_client/pubspec.yaml`

```yaml
name: local_storage_client
description: Client for local key-value storage.
version: 0.1.0+1
publish_to: none

environment:
  sdk: ^3.11.0

dependencies:
  shared_preferences: ^2.5.0

dev_dependencies:
  mocktail: ^1.0.0
  test: ^1.25.0
  very_good_analysis: ^7.0.0
```

`packages/local_storage_client/lib/local_storage_client.dart`

```dart
/// 로컬 키·값 저장소 클라이언트.
library;

export 'src/local_storage_client.dart';
```

`packages/local_storage_client/lib/src/local_storage_client.dart`

```dart
import 'package:shared_preferences/shared_preferences.dart';

/// 로컬 키·값 저장소 클라이언트.
class LocalStorageClient {
  LocalStorageClient({
    required SharedPreferences sharedPreferences,
  }) : _sharedPreferences = sharedPreferences;

  final SharedPreferences _sharedPreferences;

  /// [key]의 문자열 값을 읽는다.
  String? read(String key) => _sharedPreferences.getString(key);

  /// [key]에 문자열 [value]를 저장한다.
  Future<void> write(String key, String value) async {
    await _sharedPreferences.setString(key, value);
  }

  /// [key]의 값을 제거한다.
  Future<void> delete(String key) async {
    await _sharedPreferences.remove(key);
  }
}
```

## 저장소 계층: user_repository

`packages/user_repository/pubspec.yaml`

```yaml
name: user_repository
description: Repository for user data.
version: 0.1.0+1
publish_to: none

environment:
  sdk: ^3.11.0

dependencies:
  equatable: ^2.0.7
  local_storage_client:
    path: ../local_storage_client
  user_api_client:
    path: ../user_api_client

dev_dependencies:
  mocktail: ^1.0.0
  test: ^1.25.0
  very_good_analysis: ^7.0.0
```

`packages/user_repository/lib/user_repository.dart`

```dart
/// 사용자 데이터 저장소.
library;

export 'src/models/models.dart';
export 'src/user_repository.dart';
```

`packages/user_repository/lib/src/models/models.dart`

```dart
export 'user.dart';
```

`packages/user_repository/lib/src/models/user.dart`

```dart
import 'package:equatable/equatable.dart';

/// 사용자를 표현하는 도메인 모델.
class const User({
  required final String id,
  required final String email,
  required final String displayName,
  final String? avatarUrl,
}) extends Equatable {
  @override
  List<Object?> get props => [id, email, displayName, avatarUrl];
}
```

`packages/user_repository/lib/src/user_repository.dart`

```dart
import 'package:user_api_client/user_api_client.dart';
import 'package:user_repository/user_repository.dart';

/// 사용자를 찾지 못했을 때 발생하는 예외.
class const UserNotFoundException(final String userId) implements Exception;

/// 사용자 데이터 저장소.
///
/// [UserApiClient]와 로컬 캐시를 결합해
/// 비즈니스 로직 계층에 사용자 데이터를 제공한다.
class UserRepository {
  const UserRepository({
    required UserApiClient userApiClient,
  }) : _userApiClient = userApiClient;

  final UserApiClient _userApiClient;

  /// 지정한 [userId]의 [User]를 반환한다.
  ///
  /// 사용자가 없으면 [UserNotFoundException]을 던진다.
  Future<User> getUser(String userId) async {
    try {
      final response = await _userApiClient.getUser(userId);
      return User(
        id: response.id,
        email: response.email,
        displayName: response.displayName,
        avatarUrl: response.avatarUrl,
      );
    } on UserApiException catch (e) {
      if (e.statusCode == 404) {
        throw UserNotFoundException(userId);
      }
      rethrow;
    }
  }
}
```

## 비즈니스 로직: ProfileBloc

`lib/profile/bloc/profile_event.dart`

```dart
part of 'profile_bloc.dart';

sealed class ProfileEvent extends Equatable {
  const ProfileEvent();

  @override
  List<Object> get props => [];
}

final class const ProfileLoadRequested({required final String userId})
    extends ProfileEvent {
  @override
  List<Object> get props => [userId];
}
```

`lib/profile/bloc/profile_state.dart`

```dart
part of 'profile_bloc.dart';

sealed class ProfileState extends Equatable {
  const ProfileState();

  @override
  List<Object?> get props => [];
}

final class ProfileInitial extends ProfileState {
  const ProfileInitial();
}

final class ProfileLoading extends ProfileState {
  const ProfileLoading();
}

final class const ProfileSuccess({required final User user})
    extends ProfileState {
  @override
  List<Object?> get props => [user];
}

final class ProfileNotFound extends ProfileState {
  const ProfileNotFound();
}

final class ProfileFailure extends ProfileState {
  const ProfileFailure();
}
```

`lib/profile/bloc/profile_bloc.dart`

```dart
import 'package:equatable/equatable.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:user_repository/user_repository.dart';

part 'profile_event.dart';
part 'profile_state.dart';

class ProfileBloc extends Bloc<ProfileEvent, ProfileState> {
  ProfileBloc({
    required UserRepository userRepository,
  })  : _userRepository = userRepository,
        super(const ProfileInitial()) {
    on<ProfileLoadRequested>(_onLoadRequested);
  }

  final UserRepository _userRepository;

  Future<void> _onLoadRequested(
    ProfileLoadRequested event,
    Emitter<ProfileState> emit,
  ) async {
    emit(const ProfileLoading());
    try {
      final user = await _userRepository.getUser(event.userId);
      emit(ProfileSuccess(user: user));
    } on UserNotFoundException {
      emit(const ProfileNotFound());
    } catch (_) {
      emit(const ProfileFailure());
    }
  }
}
```

## 화면: Page와 View

`lib/profile/view/profile_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:my_app/profile/bloc/profile_bloc.dart';
import 'package:my_app/profile/view/profile_view.dart';
import 'package:user_repository/user_repository.dart';

class const ProfilePage({required final String userId, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => ProfileBloc(
        userRepository: context.read<UserRepository>(),
      )..add(ProfileLoadRequested(userId: userId)),
      child: const ProfileView(),
    );
  }
}
```

`lib/profile/view/profile_view.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:my_app/profile/bloc/profile_bloc.dart';

class ProfileView extends StatelessWidget {
  const ProfileView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: BlocBuilder<ProfileBloc, ProfileState>(
        builder: (context, state) {
          return switch (state) {
            ProfileInitial() => const SizedBox.shrink(),
            ProfileLoading() => const Center(
                child: CircularProgressIndicator(),
              ),
            ProfileSuccess(:final user) => Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      user.displayName,
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    const SizedBox(height: 8),
                    Text(user.email),
                  ],
                ),
              ),
            ProfileNotFound() => const Center(
                child: Text('User not found'),
              ),
            ProfileFailure() => const Center(
                child: Text('Something went wrong'),
              ),
          };
        },
      ),
    );
  }
}
```

## 부트스트랩 연결

`lib/main_development.dart`

```dart
import 'package:flutter/material.dart';
import 'package:my_app/app/app.dart';
import 'package:user_api_client/user_api_client.dart';
import 'package:user_repository/user_repository.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  const baseUrl = 'https://api.dev.example.com';

  final userApiClient = UserApiClient(baseUrl: baseUrl);
  final userRepository = UserRepository(userApiClient: userApiClient);

  runApp(
    App(userRepository: userRepository),
  );
}
```

`lib/app/view/app.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:user_repository/user_repository.dart';

class const App({
  required final UserRepository userRepository,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return RepositoryProvider.value(
      value: userRepository,
      child: const MaterialApp(
        home: HomePage(),
      ),
    );
  }
}
```

환경별 진입점에서 클라이언트·저장소를 구성하고 App에 넘긴다. 환경마다 설정을 바꾸되 연결 구조는 유지한다.

```dart
// lib/main_development.dart
import 'package:auth_api_client/auth_api_client.dart';
import 'package:auth_repository/auth_repository.dart';
import 'package:flutter/material.dart';
import 'package:local_storage_client/local_storage_client.dart';
import 'package:my_app/app/app.dart';
import 'package:user_api_client/user_api_client.dart';
import 'package:user_repository/user_repository.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  const baseUrl = 'https://api.dev.example.com';

  // 데이터 계층
  final authApiClient = AuthApiClient(baseUrl: baseUrl);
  final userApiClient = UserApiClient(baseUrl: baseUrl);
  final localStorageClient = LocalStorageClient();

  // 저장소 계층
  final authRepository = AuthRepository(
    authApiClient: authApiClient,
    localStorageClient: localStorageClient,
  );
  final userRepository = UserRepository(
    userApiClient: userApiClient,
  );

  runApp(
    App(
      authRepository: authRepository,
      userRepository: userRepository,
    ),
  );
}
```
