---
name: flutter-layered-architecture
description: "Flutter 앱의 패키지·폴더 배치, 데이터·저장소·Bloc·화면의 계층 경계와 부트스트랩을 설계하거나 수정할 때 사용한다."
---

# 계층형 Flutter 아키텍처

데이터, 저장소, 비즈니스 로직, 화면의 네 계층을 단방향으로 연결한다. 새 구조를 설계하거나 기존 계층 경계를 수정할 때 사용하며, 요청하지 않은 앱 전체 재구성은 하지 않는다.

## 핵심 기준

- 의존 방향은 화면 → 비즈니스 로직 → 저장소 → 데이터다.
- 데이터·저장소는 각각 `pubspec.yaml`을 가진 `packages/`의 독립 Dart 패키지에 둔다. 비즈니스 로직·화면은 앱 `lib/`의 기능별 폴더에 둔다.
- 데이터 패키지는 외부 통신만 담당하며 도메인 규칙을 포함하지 않는다. 데이터·저장소 패키지는 Flutter SDK에 의존하지 않는다.
- 저장소는 도메인별로 나누고 서로 직접 의존하지 않는다. 필요한 조합은 비즈니스 로직에서 처리한다.
- 로컬 패키지는 `path:` 의존성을 사용한다. 공개 API는 배럴로 내보내고 소비자가 `src/`를 직접 가져오지 않게 한다.
- 저장소가 사용하는 모든 외부 데이터 원천을 생성자로 주입한다. SDK 싱글턴도 부트스트랩에서 만들거나 얻어 전달한다.
- 앱 진입점·부트스트랩만 데이터 패키지를 직접 가져온다. Bloc·위젯·앱 테스트는 저장소를 통해 접근한다.
- Dart 3.13 이상이면 기본 생성자의 선언 매개변수를 사용한다. 이전 SDK에서는 호환 문법을 유지한다.
- 생성·의존성·테스트는 연결된 MCP의 실제 스키마를 확인해 사용하거나 `very_good create dart_package`, `very_good packages get`, `very_good test` CLI로 수행한다.

## 계층별 책임

| 계층 | 책임 | 위치 | 의존 |
| --- | --- | --- | --- |
| 데이터 | API·저장소·외부 SDK 통신 | `packages/<name>_api_client/` | 외부 패키지 |
| 저장소 | 원천 조합·모델 변환·캐시 | `packages/<name>_repository/` | 필요한 데이터 패키지 |
| 비즈니스 로직 | 사용자 동작과 상태 전이 | `lib/<feature>/bloc/` 또는 `cubit/` | 저장소 |
| 화면 | Page·View·Widget·배치 | `lib/<feature>/view/` | 비즈니스 로직 |

```text
┌─────────────────────────────────────────────┐
│              화면 계층                      │
│          (lib/<feature>/view/)              │
└──────────────────┬──────────────────────────┘
                   │ 상태 읽기·이벤트 전달
┌──────────────────▼──────────────────────────┐
│            비즈니스 로직                    │
│        (lib/<feature>/bloc/)                │
└──────────────────┬──────────────────────────┘
                   │ 저장소 메서드 호출
┌──────────────────▼──────────────────────────┐
│              저장소 계층                    │
│      (packages/<name>_repository/)          │
└──────────────────┬──────────────────────────┘
                   │ 데이터 클라이언트 호출
┌──────────────────▼──────────────────────────┐
│               데이터 계층                    │
│     (packages/<name>_api_client/)           │
└─────────────────────────────────────────────┘
```

## 모노레포 배치

기능마다 bloc/cubit과 view를 나누고 배럴을 둔다. 데이터 원천과 저장소마다 별도 패키지를 만든다.

```text
my_app/
├── lib/
│   ├── app/
│   │   ├── app.dart                          # 공개 API 배럴
│   │   └── view/
│   │       └── app.dart                      # MultiRepositoryProvider를 사용하는 App
│   ├── login/                                # 로그인 기능
│   │   ├── login.dart                        # 공개 API 배럴
│   │   ├── bloc/
│   │   │   ├── login_bloc.dart
│   │   │   ├── login_event.dart
│   │   │   └── login_state.dart
│   │   └── view/
│   │       ├── login_page.dart               # Page가 Bloc 제공
│   │       └── login_view.dart               # View가 상태 소비
│   ├── profile/                              # 프로필 기능
│   ├── main_development.dart                 # 환경별 진입점
│   ├── main_staging.dart
│   └── main_production.dart
├── packages/
│   ├── auth_api_client/                      # 데이터 계층: 인증 API
│   │   ├── lib/
│   │   │   ├── auth_api_client.dart          # 공개 API 배럴
│   │   │   └── src/
│   │   │       ├── auth_api_client.dart
│   │   │       └── models/
│   │   │           ├── models.dart
│   │   │           └── auth_response.dart
│   │   └── pubspec.yaml
│   ├── local_storage_client/                 # 데이터 계층: 로컬 저장
│   ├── auth_repository/                      # 저장소 계층: 인증
│   │   ├── lib/
│   │   │   ├── auth_repository.dart          # 공개 API 배럴
│   │   │   └── src/
│   │   │       ├── auth_repository.dart
│   │   │       └── models/
│   │   │           ├── models.dart
│   │   │           └── user.dart             # 도메인 모델
│   │   └── pubspec.yaml
│   └── user_repository/                      # 저장소 계층: 사용자
├── test/
│   └── ...                                   # lib 구조와 대응
└── pubspec.yaml                              # 앱 루트 pubspec
```

## 데이터 계층

외부 스키마에 맞는 응답 모델과 타입이 있는 메서드를 제공한다. HTTP 클라이언트를 주입하고 모델에 `fromJson`·`toJson`을 둔다. 원시 JSON을 상위 계층에 반환하지 않는다.

```dart
/// 사용자 API용 HTTP 클라이언트.
class UserApiClient {
  // http.Client 주입: 테스트는 목, 실제 앱은 실제 클라이언트 사용
  UserApiClient({
    required String baseUrl,
    http.Client? httpClient,
  })  : _baseUrl = baseUrl,
        _httpClient = httpClient ?? http.Client();

  final String _baseUrl;
  final http.Client _httpClient;

  /// 모든 메서드는 타입이 있는 응답 모델을 반환한다.
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

[전체 예제](references/worked-example.md)에 pubspec·모델·예외·배럴이 있다.

## 저장소 계층

응답 모델을 앱의 도메인 모델로 변환한다. 도메인 모델은 저장소 패키지에 둔다. 외부 원천이 없는 메모리 상태 저장소는 불필요한 생성자 인수를 받을 필요가 없다.

```dart
/// 도메인 모델은 데이터가 아닌 저장소 패키지에 둔다.
/// API 스키마가 아니라 앱의 요구에 맞는 필드다.
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

```dart
/// 저장소는 데이터 클라이언트를 직접 만들지 않고 주입받는다.
class UserRepository {
  const UserRepository({
    required UserApiClient userApiClient,
  }) : _userApiClient = userApiClient;

  final UserApiClient _userApiClient;

  /// UserResponse 응답을 User 도메인 모델로 변환한다.
  Future<User> getUser(String userId) async {
    final response = await _userApiClient.getUser(userId);
    return User(
      id: response.id,
      email: response.email,
      displayName: response.displayName,
      avatarUrl: response.avatarUrl,
    );
  }
}
```

[모델 변환](references/model-transformation.md)과 [전체 예제](references/worked-example.md)를 참고한다.

## 의존성과 import 경계

데이터 패키지는 외부 패키지, 저장소는 데이터 패키지에 의존한다. 앱 루트는 부트스트랩이 생성하는 데이터 클라이언트와 저장소 모두를 선언해야 `depend_on_referenced_packages`를 만족한다. 선언 후에는 린트만으로 Bloc의 데이터 import를 막지 못하므로 코드 경계를 별도로 확인한다.

```yaml
# packages/user_api_client/pubspec.yaml — 외부 패키지만 의존
dependencies:
  http: ^1.4.0

# packages/user_repository/pubspec.yaml — 데이터 패키지의 path 의존
dependencies:
  user_api_client:
    path: ../user_api_client

# pubspec.yaml: 저장소와 부트스트랩이 생성하는 데이터 패키지
dependencies:
  user_api_client:
    path: packages/user_api_client
  user_repository:
    path: packages/user_repository
```

[pubspec과 import 검사](references/pubspec.md)를 참고한다.

## 데이터 흐름

화면 이벤트 → Bloc → 저장소 → 데이터 클라이언트 → 도메인 모델 → 상태 → 화면 재빌드 순서다. [단계별 예제](references/data-flow.md)를 참고한다.

## 부트스트랩

`main_<flavor>.dart`에서 클라이언트·저장소를 생성하고 `App`의 `MultiRepositoryProvider`로 제공한다. flavor는 URL 등 설정을 바꾸며 연결 구조를 중복 설계하지 않는다. 비밀키는 클라이언트 코드에 넣지 않는다.

```dart
// lib/main_development.dart
import 'package:auth_api_client/auth_api_client.dart';
import 'package:auth_repository/auth_repository.dart';
import 'package:flutter/material.dart';
import 'package:my_app/app/app.dart';
import 'package:user_api_client/user_api_client.dart';
import 'package:user_repository/user_repository.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  const baseUrl = 'https://api.dev.example.com';

  // 데이터 계층
  final authApiClient = AuthApiClient(baseUrl: baseUrl);
  final userApiClient = UserApiClient(baseUrl: baseUrl);

  // 저장소 계층
  final authRepository = AuthRepository(authApiClient: authApiClient);
  final userRepository = UserRepository(userApiClient: userApiClient);

  runApp(
    App(
      authRepository: authRepository,
      userRepository: userRepository,
    ),
  );
}
```

## 피해야 할 패턴

| 문제 | 개선 |
| --- | --- |
| 위젯이 API 직접 호출 | 이벤트 → Bloc → 저장소 → 클라이언트 |
| 저장소끼리 의존 | 각 저장소 격리, 상위 계층에서 조합 |
| 데이터 패키지에 도메인 모델 | 응답 모델과 도메인 모델 분리 |
| 저장소가 모든 비즈니스 규칙 처리 | 데이터 조합·변환과 상태 규칙 분리 |
| 로컬 패키지에 git/pub 버전 의존 | path 의존 |
| 데이터·저장소에 Flutter import | 순수 Dart 패키지 |
| 거대한 단일 저장소 | 도메인별 저장소 |
| src 직접 import | 공개 배럴 |

## 작업 절차

### 데이터 원천 추가

1. `packages/`에 `<name>_api_client` Dart 패키지를 생성한다.
2. HTTP·JSON 의존성을 추가한다.
3. `lib/src/models/`에 응답 모델과 내보내기 파일을 작성한다.
4. 클라이언트와 패키지 배럴을 작성한다.
5. `lib/` 구조에 대응하는 테스트를 작성하고 해당 패키지에서 실행한다.

### 저장소 추가

1. `<name>_repository` Dart 패키지를 생성한다.
2. 데이터 패키지의 path 의존성과 `equatable`을 추가한다.
3. 도메인 모델과 배럴을 만든다.
4. 생성자에 클라이언트를 주입하고 응답 변환을 구현한다.
5. 데이터 클라이언트를 모킹해 저장소를 테스트한다.

### 기능과 연결

1. 루트 pubspec에 저장소와 부트스트랩이 사용하는 데이터 패키지를 선언한다.
2. 진입점에서 생성해 `App`으로 넘기고 `RepositoryProvider.value`로 제공한다.
3. [Bloc 스킬](../flutter-bloc/SKILL.md)에 따라 Bloc/Cubit과 Page/View를 연결한다.
4. `lib/`·`test/`의 데이터 import가 진입점·부트스트랩에만 있는지 확인한다.

## 참고 문서

- [전체 예제](references/worked-example.md), [pubspec](references/pubspec.md)
- [데이터 흐름](references/data-flow.md), [모델 변환](references/model-transformation.md)
- [계층별 테스트](references/testing.md), [테스트 관례](../flutter-testing/SKILL.md)
