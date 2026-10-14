# UI 패키지 상세 예제

## ThemeExtension 구성

| 클래스 | 용도 |
| --- | --- |
| `AppColors extends ThemeExtension<AppColors>` | ColorScheme에 없는 success·warning·info와 on 역할 |
| `AppSpacing extends ThemeExtension<AppSpacing>` | xxs~xxlg 간격과 copyWith·lerp |
| `lightTheme`·`darkTheme` | ColorScheme과 확장을 결합한 밝은·어두운 ThemeData |
| `AppThemeBuildContext` | context.appColors·context.appSpacing 접근 |

모든 확장은 테마 애니메이션을 위해 `copyWith`·`lerp`를 구현한다. 접근자 작성과 `ThemeData.extensions` 등록을 함께 수행한다.

```dart
ThemeData get lightTheme => ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: _seedColor),
  extensions: const <ThemeExtension<dynamic>>[AppColors.light, AppSpacing()],
);

ThemeData get darkTheme => ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: _seedColor,
    brightness: Brightness.dark,
  ),
  extensions: const <ThemeExtension<dynamic>>[AppColors.dark, AppSpacing()],
);

const _seedColor = Color(0xFF6750A4);

extension AppThemeBuildContext on BuildContext {
  /// Material의 [ColorScheme]에 없는 추가 색상 토큰.
  AppColors get appColors => Theme.of(this).extension<AppColors>()!;

  /// 패키지의 간격 척도.
  AppSpacing get appSpacing => Theme.of(this).extension<AppSpacing>()!;
}
```

`primary`, `onPrimary`, `surface`, `onSurface`는 `colorScheme`에서만 읽어 정의가 이중화되지 않게 한다.

## 테스트 헬퍼

```dart
extension PumpApp on WidgetTester {
  Future<void> pumpApp(Widget widget, {ThemeData? theme}) {
    return pumpWidget(
      MaterialApp(
        theme: theme ?? lightTheme,
        home: Scaffold(body: widget),
      ),
    );
  }
}
```

## 배럴 파일

```dart
/// Material을 기반으로 하는 사용자 정의 Flutter 위젯 라이브러리.
library;

export 'package:flutter/material.dart';

export 'src/extensions/build_context_extensions.dart';
export 'src/theme/app_colors.dart';
export 'src/theme/app_spacing.dart';
export 'src/theme/app_theme.dart';
export 'src/widgets/app_button.dart';
export 'src/widgets/app_card.dart';
export 'src/widgets/app_text_field.dart';
```

## Widgetbook

- `use_cases/`에 위젯별 파일과 `@widgetbook.UseCase(name:, type:)` 최상위 함수를 둔다.
- `UseCaseDecorator`로 공통 배경을 제공한다.
- `ThemeAddon`에 `lightTheme`·`darkTheme`를 연결한다.
- `build_runner`로 주석을 읽어 `widgetbook.directories.g.dart`를 생성한다.

| 명령 | 용도 |
| --- | --- |
| `cd widgetbook && dart run build_runner build --delete-conflicting-outputs` | 사용 사례 변경 후 목록 재생성 |
| `cd widgetbook && flutter run -d chrome` | 로컬 카탈로그 실행 |

## 위젯 추가

1. `lib/src/widgets/app_<name>.dart`에 const 생성자와 문서를 작성한다.
2. Material을 조합하고 컨텍스트로 추가 토큰을 읽는다.
3. `lib/my_ui.dart`에서 내보낸다.
4. `test/src/widgets/app_<name>_test.dart`에 동작 테스트를 추가한다.
5. `widgetbook/lib/widgetbook/use_cases/app_<name>.dart`에 변형별 사례를 추가한다.
6. Widgetbook에서 생성 명령을 실행한다.

## 토큰 추가

1. 해당 ThemeExtension에 토큰을 추가한다.
2. `copyWith`·`lerp`를 갱신한다.
3. 밝은·어두운 테마 값을 지정한다.
4. 확장을 직접 생성하는 테스트를 갱신한다.
5. BuildContext 확장으로 사용한다.
