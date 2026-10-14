---
name: flutter-review
description: "변경된 Flutter/Dart 코드를 읽기 전용으로 리뷰할 때 사용한다. Effective Dart와 관련 Flutter 지침을 기준으로 정확성, 수명, 테스트, 보안과 접근성 문제를 보고한다."
---

# Flutter 변경 코드 리뷰

변경된 Dart 코드를 읽고 문제를 보고한다. 이 스킬 자체는 파일을 수정하지 않는다. Codex에서 직접 수행하며 별도의 에이전트나 전용 훅이 필요하지 않다. 현재 환경의 읽기 전용 권한과 사용자 범위를 따른다.

## 검토 기준

먼저 아래 공통 기준을 적용하고, 변경된 기능에 필요한 분야만 추가로 검토한다. 다른 스킬을 참고하더라도 리뷰의 읽기 전용 범위는 유지한다.

## 공식 기준과 프로젝트 관례

이 섹션은 구현 스킬도 공유한다. 읽기 전용 제한은 리뷰 호출에만 적용하며 구현·수정 요청의 범위를 바꾸지 않는다.

- [Effective Dart](https://dart.dev/effective-dart)의 Style·Documentation·Usage·Design을 Dart 기준으로 삼는다. Flutter는 [아키텍처 권장사항](https://docs.flutter.dev/app-architecture/recommendations), [성능](https://docs.flutter.dev/perf/best-practices), [테스트](https://docs.flutter.dev/testing/overview), [접근성](https://docs.flutter.dev/ui/accessibility)의 해당 항목을 확인한다. 이를 별도의 단일 공식 문서인 “Effective Flutter”로 인용하지 않는다.
- 공식 권고의 DO·PREFER·CONSIDER·AVOID와 언어/API 오류를 구분한다. Bloc, Equatable, mocktail, Page/View 분리, 독립 패키지, 정적 토큰 클래스, 100% 커버리지는 Flutter 공통 필수 조건이 아니다. 기존 프로젝트의 명시적 선택은 유지하며 취향 차이를 결함으로 보고하지 않는다.
- `pubspec.yaml`의 SDK **하한이 정하는 언어 버전**, 파일별 `// @dart=`, 실제 SDK와 패키지 해결 버전을 함께 확인한다. 실행 SDK가 3.13이어도 언어 버전이 낮으면 primary constructor를 사용할 수 없다. 예제를 복사하려고 SDK 하한이나 의존성을 임의로 올리지 않는다.
- 이름·문서·공개 API: 타입은 UpperCamelCase, 멤버는 lowerCamelCase, 파일은 lowercase_with_underscores로 작성하고 공개 계약을 dartdoc으로 설명한다. 단순 상수·함수를 묶기 위해 static 전용 클래스를 새로 만들기보다 최상위 선언을 우선한다. 기존 공개 API를 스타일만으로 깨뜨리지 않는다.
- 타입·불변성: 불필요한 `dynamic`·`!`·`late`를 피하고, 비동기 무반환 함수는 `Future<void>`로 선언한다. `final List`도 내용은 바뀔 수 있으므로 공유 상태에는 방어적 복사/불변 컬렉션을 고려한다. `==`와 `hashCode`는 함께 일관되게 구현한다.
- 예외·비동기: 처리 가능한 예외를 `on`으로 제한하고 예상 밖 오류를 삼키지 않는다. 다시 던질 때 `rethrow`로 스택을 보존한다. UI에는 정제된 오류만 전달한다. Future를 기다리거나 의도적 비동기 실행과 오류 처리 방식을 명시한다.
- Flutter 수명: 비동기 간격 뒤에는 사용하는 `context.mounted`/`mounted`를 확인하고 가능하면 작업 자체를 취소한다. 생성한 컨트롤러·구독·클라이언트는 소유자가 해제한다. `build`에서 요청·구독·컨트롤러 생성 같은 부수 효과를 시작하지 않는다.
- import는 다른 패키지의 `src/`를 침범하지 않는다. 같은 lib 안에서는 상대 경로가 공식 선호이며, test에서 lib로 들어갈 때는 `package:`를 쓴다. 기존 린트가 다른 일관된 정책을 채택했다면 범위 밖 import 일괄 변경은 하지 않는다.
- `dart format`과 프로젝트 분석 설정을 적용한다. Flutter의 `flutter_lints`, Dart의 `lints`가 공식 린트 기준이며 `very_good_analysis`는 별도의 더 엄격한 선택이다. 분석 통과만으로 동작·접근성·보안까지 보장하지 않는다.

## 분야별 참고

다음 문서 중 변경에 관련된 것을 읽는다. 자동으로 미리 주입되었다고 가정하지 않는다.

- [Bloc](../flutter-bloc/SKILL.md)
- [테스트](../flutter-testing/SKILL.md)
- [정적 보안](../flutter-static-security/SKILL.md)
- [접근성](../flutter-accessibility/SKILL.md)
- [계층](../flutter-layered-architecture/SKILL.md), [내비게이션](../flutter-navigation/SKILL.md)
- [테마](../flutter-material-theming/SKILL.md), [애니메이션](../flutter-animations/SKILL.md), [지역화](../flutter-internationalization/SKILL.md)

변경에 관련 없는 보안 감사나 전체 아키텍처 재설계를 확대 수행하지 않는다.

## 변경 범위

1. 저장소 루트에서 `git status --short`를 확인한다.
2. 사용자 지정 비교 범위가 있으면 우선한다. 없으면 staged·unstaged Dart 변경과 추적되지 않은 Dart 파일을 확인한다.
3. 작업 트리가 깨끗하면 확인된 기준 브랜치와의 diff를 읽는다. `main`을 추정하지 말고 저장소 설정·요청에서 기준을 찾는다.
4. 파일 전체 문맥을 읽되 검토 결과는 변경 때문에 생긴 문제에 한정한다. 모노레포는 해당 패키지 기준을 적용한다.
5. 범위를 확정할 수 없으면 이유와 필요한 정보를 보고한다. Dart 변경이 없으면 “검토할 Dart 변경이 없습니다.”라고 알린다.

Git 확인은 `--no-ext-diff --no-textconv`를 사용한다. 읽기 전용 리뷰에서 코드 수정, `applyFixes`, 포맷, 생성, 의존성 설치를 실행하지 않는다. 분석 도구도 설정을 확인하고 읽기 전용으로 사용할 수 있을 때만 보조 근거로 사용한다.

## 출력

| 위치 | 문제 | 수정 제안 | 기준 |
| --- | --- | --- | --- |
| lib/counter/counter_cubit.dart:12 | 상태의 가변 필드가 불변성을 깨뜨림 | 필드를 final로 선언 | flutter-bloc |

발견별로 실제 경로·줄, 사용자에게 미치는 영향, 구체적 수정과 관련 공식 지침 또는 프로젝트 규칙을 적는다. 근거 없는 문제나 원시 분석 경고만으로 표를 채우지 않는다. 문제가 없으면 그 사실을 명시한다. 검토 범위 밖 변경과 실행하지 않은 테스트가 있다면 짧게 덧붙인다.

원본의 OS 수준 명령 차단 훅을 이 스킬이 제공한다고 주장하지 않는다. 기술적 격리가 필요하면 호스트의 읽기 전용 권한 설정으로 실행한다.
