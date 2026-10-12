---
name: flutter-sdk-upgrade
description: "Dart·Flutter SDK와 pubspec 환경 제약, CI 버전을 갱신하거나 SDK 변경으로 생긴 의존성 충돌을 해결할 때 사용한다."
---

# Dart·Flutter SDK 업그레이드

SDK 제약과 CI 버전을 일관되게 갱신한다. 기본 변경 범위는 SDK와 그 검증에 필요한 파일이며 사용자가 추가로 요청한 호환성 수정도 범위에 포함한다. 예제 CI 공급자를 기존 프로젝트에 강제하지 않는다.

## 핵심 기준

- Flutter 버전과 번들 Dart 버전은 다르다. `environment.sdk`에는 Dart 버전을 쓴다.
- 대상 Flutter의 Dart 버전은 [공식 릴리스 아카이브](https://docs.flutter.dev/install/archive) 또는 대상 SDK의 실제 버전 출력으로 확인한다. 기억으로 추정하지 않는다.
- 요청에 목표 버전이 있으면 사용하고, 최신을 요청하면 공식 자료로 확인한다. 호스트 전용 인수 치환을 전제하지 않는다.
- 순수 Dart 패키지에는 Flutter 제약을 추가하지 않는다.
- 기존 CI 공급자·버전 고정 정책을 유지한다. 예제의 `MAJOR.MINOR.x`는 최신 패치를 허용하는 방식이며 정확한 패치 고정과 구분한다.
- `^MAJOR.MINOR.PATCH`는 정확한 버전 고정이 아니라 호환 버전 범위다. 사용자가 정확한 고정을 원하면 그 요구를 따른다.
- 각 대상 패키지의 의존성 해결과 분석 결과를 확인한다. 충돌 해결을 위해 승인 범위 밖의 의존성을 무작정 바꾸지 않는다.

## 1. 목표 확인

요청과 프로젝트에서 목표 Flutter·Dart 버전을 확인해 알린다. 둘 다 명확하면 재확인으로 멈추지 않는다. 네트워크와 대상 SDK가 모두 없어 매핑을 확인할 수 없으면 필요한 버전만 질문하고 독립적으로 할 수 있는 파일 조사를 진행한다.

## 2. CI

실제 `.github/workflows/`와 버전 관리 파일을 읽는다. Flutter 작업에는 Flutter 버전을, 순수 Dart 작업에는 Dart 버전을 넣는다. 기존 재사용 워크플로를 사용하는 경우 다음 형태를 참고하되 공급자와 태그를 임의로 교체하지 않는다.

Flutter 예제:

```yaml
with:
  flutter_version: "3.41.x" # MAJOR.MINOR.x 범위의 최신 패치
```

Dart 예제:

```yaml
with:
  dart_sdk: "3.11.0" # 정확한 Dart 버전, Flutter 버전과 구분
```

워크플로 파일을 보지 못했다면 예시 블록이라는 점을 밝힌다. 존재하지 않는 jobs·name·on 구조를 만들어 사실처럼 제시하지 않는다.

```yaml
# 순수 Dart 3.11.0을 목표로 하는 매개변수 예제, 기존 작업의 스키마 확인 필요
with:
  dart_sdk: "3.11.0"
```

## 3. pubspec 환경 제약

Flutter 의존성이 있는 패키지:

```yaml
environment:
  sdk: ^<dart-version> # 대상 Flutter가 제공하는 Dart 버전
  flutter: ^<flutter-version> # 대상 Flutter 버전
```

Flutter와 Dart 자리표시자는 각각 확인한 버전으로 채운다. 숫자가 우연히 같거나 다르다는 규칙이 아니라 실제 SDK 조합이 기준이다.

순수 Dart:

```yaml
environment:
  sdk: ^3.11.0 # Dart 버전만 지정
  # Flutter 제약 없음
```

모노레포의 각 pubspec과 workspace의 공유 SDK 정책을 확인한다.

## 4. 검증

MCP가 연결되어 있으면 지원하는 도구를 사용하고 아니면 해당 패키지에서 CLI를 실행한다.

```bash
flutter pub get   # 순수 Dart는 dart pub get
flutter analyze   # 순수 Dart는 dart analyze
```

Pub workspace라면 실제 workspace 해결 범위를 따르고, 독립 패키지는 각각 확인한다. 새 분석 오류와 기존 오류를 구분한다. 충돌은 패키지·버전·서로 충돌하는 제약을 보고한다. [충돌 해석](references/version-conflicts.md)을 참고한다.

## 5. 범위 관리

SDK만 요청한 작업에서는 관련 없는 의존성·기능 변경을 섞지 않는다. 아래는 SDK만 바꾸는 예시다.

```yaml
environment:
  sdk: ^<dart-version> # 아카이브에서 확인한 Dart 버전
  flutter: ^<flutter-version> # 대상 Flutter 버전

dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.0 # SDK만 요청한 예제에서는 기존 의존성 유지
```

사용자가 의존성 갱신과 오류 수정도 요청했다면 이를 일괄 거부하지 않는다. 필요한 범위와 위험을 설명하고 승인된 호환성 수정을 진행한다. 서로 독립적인 변경은 리뷰하기 쉽게 나눌 수 있다.

## 6. 변경 검토

의도한 CI·pubspec·버전 설정·필요한 lockfile 및 호환성 수정만 남았는지 확인한다.

```bash
git diff HEAD --name-only
```

사용자가 커밋·PR 작업을 요청한 경우 프로젝트 규칙을 따르고 검증 결과와 두 SDK 버전을 기록한다. 다음은 메시지 예시이며 외부 게시를 자동으로 허용하지 않는다.

```text
chore: Flutter <flutter-version> / Dart <dart-version> 업그레이드

- 기존 CI의 SDK 설정 갱신
- 각 pubspec의 environment 제약 갱신
- 검증 결과와 필요한 호환성 변경 기록
```
