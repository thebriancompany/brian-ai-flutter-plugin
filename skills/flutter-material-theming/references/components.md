# 컴포넌트 테마

Material 컴포넌트는 기본적으로 `colorScheme`·`textTheme`을 사용한다. 추가 스타일은 위젯마다 지정하지 않고 `ThemeData`에 모은다.

아래는 정규화된 InputDecorationThemeData·AppBarThemeData API를 사용한다. [마이그레이션 안내](https://docs.flutter.dev/release/breaking-changes/component-theme-normalization)와 대상 SDK를 확인하고 구버전은 해당 버전 타입을 유지한다.

## FilledButton

```dart
ThemeData(
  filledButtonTheme: FilledButtonThemeData(
    style: FilledButton.styleFrom(
      minimumSize: const Size(72, 48),
      textStyle: appLabelLarge,
    ),
  ),
)
```

## InputDecoration

```dart
ThemeData(
  inputDecorationTheme: InputDecorationThemeData(
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
    ),
    contentPadding: EdgeInsets.symmetric(
      horizontal: spacingLg,
      vertical: spacingMd,
    ),
  ),
)
```

## AppBar

```dart
ThemeData(
  appBarTheme: AppBarThemeData(
    centerTitle: true,
    elevation: 0,
    titleTextStyle: appTitleLarge,
  ),
)
```

## 전체 테마

```dart
ThemeData get lightTheme {
  final colorScheme = ColorScheme(
    brightness: Brightness.light,
    primary: brandPrimaryColor,
    secondary: brandSecondaryColor,
    error: brandErrorColor,
    surface: brandSurfaceColor,
    onPrimary: Colors.white,
    onSecondary: Colors.white,
    onError: Colors.white,
    onSurface: Colors.black,
  );

  return ThemeData(
    colorScheme: colorScheme,
    textTheme: TextTheme(
      displayLarge: appDisplayLarge,
      headlineMedium: appHeadlineMedium,
      titleLarge: appTitleLarge,
      bodyLarge: appBodyLarge,
      labelLarge: appLabelLarge,
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        minimumSize: const Size(72, 48),
        textStyle: appLabelLarge,
      ),
    ),
    inputDecorationTheme: InputDecorationThemeData(
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
    ),
    appBarTheme: AppBarThemeData(
      centerTitle: true,
      elevation: 0,
      titleTextStyle: appTitleLarge,
    ),
  );
}
```

## 테마 적용

```dart
MaterialApp(
  theme: lightTheme,
  darkTheme: darkTheme,
  home: const HomePage(),
)
```

## 위젯에서 테마 속성 읽기

```dart
@override
Widget build(BuildContext context) {
  final theme = Theme.of(context);
  final colorScheme = theme.colorScheme;
  final textTheme = theme.textTheme;

  return ColoredBox(
    color: colorScheme.surface,
    child: Text('Good', style: textTheme.bodyLarge),
  );
}
```
