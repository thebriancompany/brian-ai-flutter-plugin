# 데이터 흐름 예제

사용자가 프로필 불러오기 버튼을 누르는 흐름이다.

## 1. 화면에서 이벤트 전달

```dart
// lib/profile/view/profile_view.dart
ElevatedButton(
  onPressed: () {
    context.read<ProfileBloc>().add(
      const ProfileLoadRequested(userId: '123'),
    );
  },
  child: const Text('Load Profile'),
)
```

## 2. 비즈니스 로직에서 저장소 호출

```dart
// lib/profile/bloc/profile_bloc.dart
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
```

## 3. 저장소에서 데이터 클라이언트 호출

API의 404는 저장소의 `UserNotFoundException`으로 변환해 Bloc이 `ProfileNotFound`를 표시하도록 한다. 나머지 API 응답 오류는 도메인 예외 UserLoadException으로 변환한다. 예외 정의는 [전체 예제](worked-example.md)를 참고한다.

```dart
// packages/user_repository/lib/src/user_repository.dart
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
```

## 4. 외부 원천과 통신

```dart
// packages/user_api_client/lib/src/user_api_client.dart
Future<UserResponse> getUser(String userId) async {
  final response = await _httpClient.get(Uri.parse('$_baseUrl/users/$userId'));

  if (response.statusCode != 200) {
    throw UserApiException(response.statusCode, response.body);
  }

  return UserResponse.fromJson(
    json.decode(response.body) as Map<String, dynamic>,
  );
}
```

## 5. 도메인 데이터와 상태를 받아 화면 재빌드

```dart
// lib/profile/view/profile_view.dart
BlocBuilder<ProfileBloc, ProfileState>(
  builder: (context, state) {
    return switch (state) {
      ProfileInitial() => const SizedBox.shrink(),
      ProfileLoading() => const CircularProgressIndicator(),
      ProfileSuccess(:final user) => ProfileContent(user: user),
      ProfileNotFound() => const Text('User not found'),
      ProfileFailure() => const Text('Something went wrong'),
    };
  },
)
```
