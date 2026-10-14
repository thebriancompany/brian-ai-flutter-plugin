# pubspec.yaml 참조

## 데이터 패키지

```yaml
name: weather_api_client
description: HTTP client for the Weather API.
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

## 저장소 패키지

```yaml
name: weather_repository
description: Repository for weather data.
version: 0.1.0+1
publish_to: none

environment:
  sdk: ^3.11.0

dependencies:
  equatable: ^2.0.7
  weather_api_client:
    path: ../weather_api_client

dev_dependencies:
  mocktail: ^1.0.0
  test: ^1.25.0
  very_good_analysis: ^7.0.0
```

## 앱 루트

```yaml
name: my_app
description: Flutter 애플리케이션.
version: 1.0.0+1
publish_to: none

environment:
  sdk: ^3.11.0
  flutter: ^3.29.0

dependencies:
  flutter:
    sdk: flutter
  flutter_bloc: ^9.1.0
  auth_api_client:
    path: packages/auth_api_client
  auth_repository:
    path: packages/auth_repository
  user_api_client:
    path: packages/user_api_client
  user_repository:
    path: packages/user_repository
  weather_api_client:
    path: packages/weather_api_client
  weather_repository:
    path: packages/weather_repository

dev_dependencies:
  bloc_test: ^10.0.0
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.0
  very_good_analysis: ^7.0.0

flutter:
  uses-material-design: true
```

## 공유 Flutter 패키지

공유 위젯·테마처럼 Flutter SDK가 필요한 경우다.

```yaml
name: app_ui
description: Shared UI components and theme for the app.
version: 0.1.0+1
publish_to: none

environment:
  sdk: ^3.11.0
  flutter: ^3.29.0

dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  very_good_analysis: ^7.0.0
```

## 의존 방향

앱 부트스트랩이 데이터 클라이언트를 생성하므로 루트 앱은 두 계층을 모두 선언한다.

### 데이터 패키지

```yaml
dependencies:
  # 외부 패키지만 사용, 로컬 의존성 없음
  http: ^1.4.0
  json_annotation: ^4.9.0
```

### 저장소 패키지

```yaml
dependencies:
  equatable: ^2.0.7
  # 데이터 계층의 path 의존
  user_api_client:
    path: ../user_api_client
```

### 앱 루트

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_bloc: ^9.1.0
  # 저장소와 환경별 진입점이 생성하는 데이터 패키지
  auth_api_client:
    path: packages/auth_api_client
  auth_repository:
    path: packages/auth_repository
  user_api_client:
    path: packages/user_api_client
  user_repository:
    path: packages/user_repository
```

## import 경계

데이터 패키지를 의존성에 선언하면 린트가 Bloc의 직접 import를 막지 못한다. 앱의 진입점·부트스트랩만 데이터 패키지를 가져오게 한다.

일반적인 허용 파일은 `lib/main_<flavor>.dart`, `lib/bootstrap.dart`, 단일 환경에서는 `lib/main.dart`다. 폴더로 나눈 프로젝트라면 실제 클라이언트 조립 파일을 기준으로 판단한다.

```text
^(import|export) 'package:user_api_client/
```

모든 검색 결과가 해당 진입점·부트스트랩이면 통과한다.

- Bloc·위젯이 데이터 모델·열거형·예외를 사용하면 저장소의 도메인 타입과 변환으로 대체한다.
- 클라이언트 직접 호출을 저장소 호출로 바꾼다.
- 앱 테스트는 클라이언트가 아니라 저장소를 모킹한다.
- 래퍼 없이 사용하는 `firebase_auth`·`firebase_storage` 같은 외부 SDK도 동일한 경계에 포함해 이름으로 검색한다.
