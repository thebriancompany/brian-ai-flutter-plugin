---
name: flutter-ui-package
description: "Flutter 공유 UI 패키지를 생성하거나 위젯·디자인 토큰·공개 API·테스트를 추가할 때 사용한다. Material과 ThemeExtension, Widgetbook 구조를 다룬다."
---

# UI 패키지

Material 위젯 위에 앱 전용 컴포넌트와 `ThemeExtension` 디자인 토큰을 구성한다. 색상·서체·간격·다크 모드의 기초는 [Material 테마](../flutter-material-theming/SKILL.md)를 함께 참고한다.

공식 권고와 팀 관례의 구분, SDK·언어 버전, 오류·수명 처리는 [공통 기준](../flutter-review/SKILL.md#공식-기준과-프로젝트-관례)을 적용한다.

## 핵심 기준

- 새 UI 패키지는 지원되는 경우 `very_good create app_ui_package` 템플릿을 사용한다. 테마·내보내기 파일·테스트 헬퍼·Widgetbook이 포함된다. 실행 전 설치된 CLI의 `--help`로 템플릿 지원 여부를 확인한다.
- `flutter/material.dart`와 Material 컴포넌트를 조합한다. 이미 있는 버튼·입력 기본 요소를 다시 만들지 않는다.
- 파일명은 lowercase_with_underscores를 사용한다. 공개 위젯별 파일 분리는 기본 관례이며 작고 밀접한 타입을 같은 라이브러리에 둘 수도 있다.
- 공개 위젯·테마를 배럴 파일에서 내보낸다. `material.dart` 전체 재노출은 패키지 API 정책으로 선택하며 필수는 아니다. 소비자는 `package:<name>/src/...`를 직접 가져오지 않는다. 사용하지 않는 코드는 트리 셰이킹 대상이 된다.
- 기본 색상 역할은 `ColorScheme`, 서체는 `TextTheme`에 둔다. 추가 토큰만 `ThemeExtension`에 넣고 `ThemeData.extensions`에 등록한 뒤 `BuildContext` 확장으로 읽는다.
- 위젯 동작·콜백·상태를 패키지의 `pumpApp` 헬퍼로 테스트한다.
- 공개 클래스에는 `App` 같은 일관된 접두사를 쓰고 가능한 생성자는 `const`로 선언한다. 공개 클래스·매개변수·메서드에 dartdoc을 쓴다.
- 피해야 할 구조를 발견하면 이유와 작동하는 개선안을 제공한다. 사용자 선택과 기존 공개 API를 존중한다.

## 패키지 구조

```text
my_ui/
├── lib/
│   ├── my_ui.dart              # 배럴 — material.dart와 공개 API 내보내기
│   └── src/
│       ├── theme/
│       │   ├── app_theme.dart        # 밝은·어두운 ThemeData 구성
│       │   ├── app_colors.dart       # 추가 색상 토큰 ThemeExtension
│       │   ├── app_spacing.dart      # 간격 토큰 ThemeExtension
│       │   └── app_text_styles.dart  # 선택적 추가 텍스트 스타일
│       ├── widgets/
│       │   ├── app_button.dart
│       │   ├── app_text_field.dart
│       │   ├── app_card.dart
│       │   └── ...
│       └── extensions/
│           └── build_context_extensions.dart  # context.appColors·context.appSpacing 접근자
├── test/
│   ├── src/
│   │   ├── theme/
│   │   │   └── app_theme_test.dart
│   │   └── widgets/
│   │       ├── app_button_test.dart
│   │       └── ...
│   └── helpers/
│       └── pump_app.dart         # MaterialApp과 테마를 제공하는 테스트 헬퍼
├── widgetbook/                   # Widgetbook 카탈로그
│   └── ...
└── pubspec.yaml
```

## 위젯 API

- `FilledButton`, `OutlinedButton`, `TextField`, `Card` 등을 조합한다.
- 최소한의 매개변수만 받고 새 위젯 API에서는 `super.key`와 `child`·`children`을 포함해 명명된 인수를 우선한다. 기존 Flutter API의 위치 인수는 그대로 따른다.
- 기본값은 테마에서 얻는다.
- 콜백은 `VoidCallback`, `ValueChanged<T>` 또는 구체적 typedef로 선언한다.
- 선택적 슬롯은 `Widget?`로 제공한다.

## 피해야 할 패턴

| 패턴 | 개선 |
| --- | --- |
| GestureDetector와 DecoratedBox로 기본 버튼 재구현 | Material 버튼 조합 |
| 독립적인 InheritedWidget 테마 체계 | ThemeData와 ThemeExtension |
| 위젯의 직접 색상 지정 | ColorScheme 또는 추가 토큰 |
| ColorScheme 역할을 별도 토큰에 중복 | success·warning·info 등 없는 값만 확장 |
| dynamic·Object·Function 콜백 | 구체적 콜백 타입 |
| 내부 파일 직접 공개 | 단일 배럴 API |

## 생성

연결된 CLI MCP가 있으면 실제 도구 스키마를 확인하고 `create`를 사용한다. 없으면 셸에서 `very_good create app_ui_package <package_name> --output-directory <dir>`를 실행한다. 이름은 snake_case, 출력 위치는 요청한 공유 패키지 폴더로 지정한다. 의존성 설치도 새 패키지 디렉터리에서 수행한다. 도구가 없다면 설치 여부를 확인하고 해결 방법을 안내한다.

[상세 예제](reference.md)에는 확장 등록·테스트 헬퍼·배럴·Widgetbook과 위젯/토큰 추가 절차가 있다.
