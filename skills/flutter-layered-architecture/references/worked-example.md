# 사용자 프로필 전체 예제

네 계층의 핵심 파일을 연결한 예제다. 앱 루트 pubspec·배럴 등 주변 설정은 [pubspec 참고](pubspec.md)에 맞춘다. 이 파일의 모델은 Dart 3.11 하한과 코드 생성 호환성을 위해 일반 생성자로 작성했다. 화면 문자열은 흐름 설명용이므로 실제 앱에서는 지역화한다.

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
class UserResponse {
  const UserResponse({
    required this.id,
    required this.email,
    required this.displayName,
    this.avatarUrl,
  });

  final String id;
  final String email;
  @JsonKey(name: 'display_name')
  final String displayName;
  @JsonKey(name: 'avatar_url')
  final String? avatarUrl;
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
class UserApiException implements Exception {
  const UserApiException(this.statusCode, this.message);

  final int statusCode;
  final String message;
}

/// 사용자 API용 HTTP 클라이언트.
class UserApiClient {
  UserApiClient({required String baseUrl, http.Client? httpClient})
    : _baseUrl = baseUrl,
      _httpClient = httpClient ?? http.Client(),
      _ownsHttpClient = httpClient == null;

  final String _baseUrl;
  final http.Client _httpClient;
  final bool _ownsHttpClient;

  /// 주입된 클라이언트는 호출자가, 내부 생성 클라이언트는 이 객체가 해제한다.
  void close() {
    if (_ownsHttpClient) _httpClient.close();
  }

  /// 지정한 [userId]의 사용자를 조회한다.
  Future<UserResponse> getUser(String userId) async {
    // 빈 ID와 경로 탐색 세그먼트는 요청 전에 거부한다.
    if (userId.isEmpty || userId == '.' || userId == '..') {
      throw ArgumentError.value(userId, 'userId', '유효한 사용자 ID가 필요합니다.');
    }
    final usersUri = Uri.parse('$_baseUrl/users');
    final response = await _httpClient.get(
      usersUri.replace(pathSegments: [...usersUri.pathSegments, userId]),
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
  flutter:
    sdk: flutter
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
  LocalStorageClient({required SharedPreferences sharedPreferences})
    : _sharedPreferences = sharedPreferences;

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
class User extends Equatable {
  const User({
    required this.id,
    required this.email,
    required this.displayName,
    this.avatarUrl,
  });

  final String id;
  final String email;
  final String displayName;
  final String? avatarUrl;
  @override
  List<Object?> get props => [id, email, displayName, avatarUrl];
}
```

`packages/user_repository/lib/src/user_repository.dart`

```dart
import 'package:user_api_client/user_api_client.dart';
import 'package:user_repository/user_repository.dart';

/// 사용자를 찾지 못했을 때 발생하는 예외.
class UserNotFoundException implements Exception {
  const UserNotFoundException(this.userId);

  final String userId;
}

/// 사용자 조회 실패를 나타내는 도메인 예외. 응답 본문은 노출하지 않는다.
class UserLoadException implements Exception {
  const UserLoadException(this.statusCode);

  final int statusCode;
}

/// 사용자 데이터 저장소.
///
/// [UserApiClient]의 응답을 변환해
/// 비즈니스 로직 계층에 사용자 데이터를 제공한다.
class UserRepository {
  const UserRepository({required UserApiClient userApiClient})
    : _userApiClient = userApiClient;

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
      throw UserLoadException(e.statusCode);
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

final class ProfileLoadRequested extends ProfileEvent {
  const ProfileLoadRequested({required this.userId});

  final String userId;
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

final class ProfileSuccess extends ProfileState {
  const ProfileSuccess({required this.user});

  final User user;
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
  ProfileBloc({required UserRepository userRepository})
    : _userRepository = userRepository,
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
    } on Exception catch (error, stackTrace) {
      addError(error, stackTrace);
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

class ProfilePage extends StatelessWidget {
  const ProfilePage({required this.userId, super.key});

  final String userId;
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) =>
          ProfileBloc(userRepository: context.read<UserRepository>())
            ..add(ProfileLoadRequested(userId: userId)),
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
            ProfileNotFound() => const Center(child: Text('User not found')),
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
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:user_api_client/user_api_client.dart';
import 'package:user_repository/user_repository.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  const baseUrl = 'https://api.dev.example.com';

  runApp(
    MultiRepositoryProvider(
      providers: [
        RepositoryProvider<UserApiClient>(
          create: (_) => UserApiClient(baseUrl: baseUrl),
          dispose: (_, client) => client.close(),
        ),
        RepositoryProvider<UserRepository>(
          create: (context) =>
              UserRepository(userApiClient: context.read<UserApiClient>()),
        ),
      ],
      child: const App(),
    ),
  );
}
```

`lib/app/view/app.dart`

```dart
import 'package:flutter/material.dart';

import '../../profile/view/profile_page.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: ProfilePage(userId: '123'));
  }
}
```

환경별 진입점은 baseUrl 등 설정만 달리하고 연결 구조는 유지한다. 위 예제는 앱 루트의 RepositoryProvider가 HTTP 클라이언트를 생성·해제한다. `.value`로 제공한 객체는 Provider가 자동 해제하지 않는다.

선택적으로 SharedPreferences 기반 어댑터가 필요하면 Flutter 패키지로 구성하고 비동기 초기화 후 주입한다. 위 user_repository 예제는 해당 어댑터를 사용하지 않으므로 의존하지 않는다.

```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final preferences = await SharedPreferences.getInstance();
  final localStorageClient = LocalStorageClient(sharedPreferences: preferences);
  // 실제로 이 어댑터를 사용하는 저장소에 주입한 뒤 runApp을 호출한다.
}
```

기존 SharedPreferences API를 사용하는 예제다. 새 구현은 패키지의 SharedPreferencesAsync/WithCache 권장사항과 대상 플랫폼을 확인한다.
