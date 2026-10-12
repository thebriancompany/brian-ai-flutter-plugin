---
name: flutter-lint-upgrade
description: "very_good_analysis 린트 패키지를 갱신하고 새 규칙의 경고를 최소 변경으로 해결할 때 사용한다. SDK 자체 업그레이드와 구분한다."
---

# Dart·Flutter 린트 업그레이드

`very_good_analysis` 버전을 올리고 새 규칙 때문에 필요한 최소 수정을 적용한다. SDK 변경이 먼저 유발한 충돌은 [SDK 업그레이드](../flutter-sdk-upgrade/SKILL.md)를 참고한다.

## 핵심 기준

- 기본 범위는 린트 버전과 새 진단의 최소 수정이다. 요청하지 않은 정리와 동작 변경을 섞지 않는다.
- 기존 버전 정책을 따르고 특별한 요구가 없다면 `^x.y.z`를 사용한다. 정확한 고정을 명시한 요청은 그대로 따른다.
- 변경 전 분석 결과를 기록해 기존 경고와 새 경고를 구분한다.
- 해결 실패 시 양쪽 제약과 의존 경로를 읽는다. 승인 없는 광범위한 의존성 갱신·제거로 강제 해결하지 않는다.
- 동작을 바꾸는 수정은 영향과 검증을 명확히 한다. 제품/API 판단이 필요한 경우에만 사용자에게 묻는다.

## 준비

요청에서 목표 버전을 읽는다. 최신 버전이 필요하면 `https://pub.dev/api/packages/very_good_analysis` 또는 공식 패키지 페이지에서 확인하고 적용 버전을 알린다.

모노레포에서는 해당 패키지를 선언한 각 pubspec을 찾는다. Pub workspace와 독립 패키지를 구분해 의존성을 해결한다. 루트 분석이 모든 패키지를 포함하는지 확인하고 포함하지 않는 패키지는 별도로 분석한다.

## 1. 버전 변경

```yaml
dev_dependencies:
  very_good_analysis: ^x.y.z # 확인한 목표 버전으로 교체
```

버전 정책별 예제:

```yaml
# 호환 범위를 원하는 경우
dev_dependencies:
  very_good_analysis: ^10.0.0 # >=10.0.0 <11.0.0: 호환 minor·patch 버전을 허용한다.

# 10.0.x의 patch 업데이트만 허용하는 경우
dev_dependencies:
  very_good_analysis: '>=10.0.0 <10.1.0'

# 정확한 버전 고정을 요청한 경우
dev_dependencies:
  very_good_analysis: 10.0.0
```

사용자가 정확한 버전을 요청했다면 캐럿 없이 쓴다. 다른 의존성·environment는 필요하고 요청된 경우에만 수정한다.

```bash
flutter pub get
```

순수 Dart에서는 `dart pub get`을 사용한다. MCP가 있으면 지원 여부와 실제 인수를 확인한다.

## 2. 분석

```bash
flutter analyze
```

순수 Dart:

```bash
dart analyze
```

전체 출력을 보관하고 기준 결과와 비교한다.

## 3. 새 진단 수정

- 새로 도입된 규칙을 해결하는 최소 변경을 한다.
- 관계없는 이름 변경·폴더 정리·기존 경고 전체 자동 수정을 피한다.
- 런타임 동작이 달라지는 캐스팅 등은 데이터 형태를 확인하고 의미 있는 테스트로 검증한다.
- 다시 분석해 새 오류가 해소되었는지 확인하고 기존 문제는 별도로 알린다.

## 4. 변경 검토와 선택적 PR

다음은 사용자가 커밋·PR까지 요청했을 때만 쓰는 예제다. 현재 작업의 관련 파일만 선택한다.

```bash
git add pubspec.yaml pubspec.lock   # 프로젝트의 lockfile 추적 정책 확인
# 린트 수정에 필요한 Dart 파일만 추가
```

메시지 예시:

```text
chore: very_good_analysis x.y.z 업그레이드

very_good_analysis를 <old>에서 <new>로 갱신하고
새 규칙으로 발생한 진단을 해결한다.
```

PR에는 실제 변경한 규칙·검증·남은 문제를 기록한다. 스킬 호출만으로 push나 게시를 수행하지 않는다.

## 경계 사례

- `analysis_options.yaml`이 이전 버전 이름을 직접 include하는지 확인한다. 새 버전과 맞지 않으면 함께 수정한다.
- 새 버전이 규칙을 제거하거나 심각도를 낮춘 결과를 오류로 취급하지 않는다.
- 사용자가 추가 정리나 의존성 업그레이드를 요청했다면 명시된 범위를 따른다. 이 스킬의 기본 범위를 이유로 거부하지 않는다.
- solver 충돌에는 양쪽 제약과 가능한 호환 버전·목표 버전 조정안을 제시한다. 일반적인 예시 버전 조합을 실제 의존성 메타데이터라고 주장하지 않는다.

[규칙별 수정 예제](references/lint-fixes.md)를 참고한다.
