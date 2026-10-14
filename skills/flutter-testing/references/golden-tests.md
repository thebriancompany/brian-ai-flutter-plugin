# 골든 이미지 테스트

렌더링 결과를 저장된 기준 이미지와 비교해 레이아웃·색상·서체·간격 변화를 검증한다.

| 대상 | 테스트 |
| --- | --- |
| 버튼의 이동 동작 | 위젯 |
| 상태별 올바른 문구 | 위젯 |
| 디자인 시각 일치 | 골든 |
| 리팩터링 후 배치 회귀 | 골든 |
| 테마별 아이콘·색상 | 골든 |

## 설정

`dart_test.yaml`에 태그를 선언한다.

```yaml
tags:
  golden:
```

공통 태그 상수를 정의한다.

```dart
// test/helpers/test_tags.dart
const goldenTag = 'golden';
```

## 테스트 작성

```dart
@Tags([goldenTag])
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../helpers/helpers.dart';

void main() {
  group(ProfileCard, () {
    testWidgets('renders correctly', (tester) async {
      await tester.pumpApp(const ProfileCard(name: 'Dash', role: 'Mascot'));

      await expectLater(
        find.byType(ProfileCard),
        matchesGoldenFile('goldens/profile_card.png'),
      );
    });
  });
}
```

## 태그 지정

파일 전체에 지정한다.

```dart
@Tags([goldenTag])
library;
```

동작 테스트와 섞여 있으면 개별 지정한다.

```dart
testWidgets('matches golden', tags: goldenTag, (tester) async {
  // ...
});
```

## 실행과 갱신

| 목적 | Flutter CLI | MCP 매개변수 예시 |
| --- | --- | --- |
| 골든만 실행 | `flutter test --tags golden` | `tags: 'golden'` |
| 기준 갱신 | `flutter test --tags golden --update-goldens` | `tags: 'golden', update_goldens: true` |
| 골든 제외 | `flutter test --exclude-tags golden` | `exclude_tags: 'golden'` |
| 모두 실행 | `flutter test` | 기본값 |

갱신한 PNG를 눈으로 검토한다. 커밋하는 작업에서는 테스트 코드와 함께 포함한다. 태그 없는 골든, 시각 비교로 동작 검증 대체, 기준 이미지 누락, 코드 속 문자열 태그 대신 태그 누락을 피한다. 실패를 숨기려고 기준 이미지를 무조건 갱신하지 않는다.
