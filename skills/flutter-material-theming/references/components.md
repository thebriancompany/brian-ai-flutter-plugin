# 컴포넌트 테마

Material 컴포넌트는 기본적으로 `colorScheme`·`textTheme`을 사용한다. 추가 스타일은 위젯마다 지정하지 않고 `ThemeData`에 모은다.

## FilledButton

```dart
ThemeData(
  filledButtonTheme: FilledButtonThemeData(
    style: FilledButton.styleFrom(
      minimumSize: const Size(72, 48),
      textStyle: AppTextStyle.labelLarge,
    ),
  ),
)
```

## InputDecoration

```dart
ThemeData(
  inputDecorationTheme: InputDecorationTheme(
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
    ),
    contentPadding: EdgeInsets.symmetric(
      horizontal: AppSpacing.lg,
      vertical: AppSpacing.md,
    ),
  ),
)
```

## AppBar

```dart
ThemeData(
  appBarTheme: AppBarTheme(
    centerTitle: true,
    elevation: 0,
    titleTextStyle: AppTextStyle.titleLarge,
  ),
)
```

## 전체 테마

```dart
class AppTheme {
  static ThemeData get light {
    final colorScheme = ColorScheme(
      brightness: Brightness.light,
      primary: AppColors.primaryColor,
      secondary: AppColors.secondaryColor,
      error: AppColors.errorColor,
      surface: AppColors.surfaceColor,
      onPrimary: Colors.white,
      onSecondary: Colors.white,
      onError: Colors.white,
      onSurface: Colors.black,
    );

    return ThemeData(
      colorScheme: colorScheme,
      textTheme: TextTheme(
        displayLarge: AppTextStyle.displayLarge,
        headlineMedium: AppTextStyle.headlineMedium,
        titleLarge: AppTextStyle.titleLarge,
        bodyLarge: AppTextStyle.bodyLarge,
        labelLarge: AppTextStyle.labelLarge,
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          minimumSize: const Size(72, 48),
          textStyle: AppTextStyle.labelLarge,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      appBarTheme: AppBarTheme(
        centerTitle: true,
        elevation: 0,
        titleTextStyle: AppTextStyle.titleLarge,
      ),
    );
  }
}
```

## 테마 적용

```dart
MaterialApp(
  theme: AppTheme.light,
  darkTheme: AppTheme.dark,
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
