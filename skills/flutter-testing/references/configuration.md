# dart_test.yaml 설정

## 설정 예제

```yaml
# dart_test.yaml — pubspec.yaml 옆 패키지 루트에 둔다.

# 테스트 분류 태그
tags:
  unit:
  integration:
  golden:

# 테스트별 기본 제한 시간
timeout: 2x

# 실행 플랫폼
platforms: [vm]

# 동시 실행 테스트 묶음 수
concurrency: 4

# 태그별 재정의
tag_overrides:
  integration:
    timeout: 4x
  golden:
    timeout: 3x

# 파일·폴더별 재정의
override_platforms:
  chrome:
    settings:
      headless: true
```

## 태그

공통 파일에 상수를 정의한다.

```dart
// test/helpers/test_tags.dart
abstract class TestTag {
  static const unit = 'unit';
  static const integration = 'integration';
  static const golden = 'golden';
}
```

파일 전체에 적용한다.

```dart
@Tags([TestTag.integration])
library;

import 'package:flutter_test/flutter_test.dart';

void main() {
  test('connects to remote service', () async {
    // ...
  });
}
```

개별 테스트에도 적용할 수 있다.

```dart
test('renders correctly', tags: TestTag.golden, () {
  // ...
});
```

## 실행

연결된 테스트 MCP가 있으면 실제 스키마를 확인한다. 다음은 지원 여부를 확인할 매개변수 예시다. 없으면 프로젝트 CLI를 사용한다.

| 목적 | MCP 매개변수 |
| --- | --- |
| Flutter 자동 감지 | 기본값 |
| 순수 Dart | `dart: true` |
| 하위 프로젝트 | `directory: 'mobile'` |
| 특정 태그 | `tags: 'unit'` |
| 태그 제외 | `exclude_tags: 'integration'` |
| 커버리지 생성 | `coverage: true` |
| 커버리지 기준 | `min_coverage: '100'`와 coverage 활성화 |
| 브라우저 | `platform: 'chrome'` |
| 순서 무작위화 | `test_randomize_ordering_seed: 'random'` |
| 모든 패키지 | `recursive: true` |
| 전체 실행 제한 | `timeout_seconds: 120` |

CLI에서는 대상 디렉터리에서 `flutter test` 또는 `dart test`를 실행한다. `very_good test`가 있으면 재귀 실행과 커버리지 기준 검사를 활용한다. 옵션은 설치 버전의 `--help`로 확인한다. 네이티브 러너로 대체할 때는 커버리지 생성·제외·기준 검사를 별도로 검증해야 한다.
