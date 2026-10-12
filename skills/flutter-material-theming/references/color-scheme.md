# ColorScheme 구성

Material 3 색상 역할을 `ThemeData` 안에서 구성한다. 사용 가능한 역할은 프로젝트 Flutter 버전에 맞춘다.

```dart
ThemeData(
  colorScheme: ColorScheme(
    brightness: Brightness.light,
    primary: AppColors.primaryColor,
    secondary: AppColors.secondaryColor,
    error: AppColors.errorColor,
    surface: AppColors.surfaceColor,
    onPrimary: Colors.white,
    onSecondary: Colors.white,
    onError: Colors.white,
    onSurface: Colors.black,
  ),
)
```

빠른 시제품은 `ColorScheme.fromSeed()`를 사용할 수 있다.

```dart
ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: AppColors.primaryColor,
  ),
)
```

## 밝은 테마와 어두운 테마

한 `AppTheme`에서 두 색상 구성을 만든다.

```dart
class AppTheme {
  static ThemeData get light => ThemeData(
    colorScheme: ColorScheme(
      brightness: Brightness.light,
      primary: AppColors.primaryColor,
      surface: AppColors.surfaceColor,
      // 나머지 색상 역할
    ),
  );

  static ThemeData get dark => ThemeData(
    colorScheme: ColorScheme(
      brightness: Brightness.dark,
      primary: AppColors.primaryColorDark,
      surface: AppColors.surfaceColorDark,
      // 나머지 색상 역할
    ),
  );
}
```

`MaterialApp`의 `theme`·`darkTheme`에 각각 전달한다.

## 위젯에서 색상 읽기

```dart
@override
Widget build(BuildContext context) {
  final colorScheme = Theme.of(context).colorScheme;

  return ColoredBox(
    color: colorScheme.surface,
    child: Text(
      'Hello',
      style: TextStyle(color: colorScheme.onSurface),
    ),
  );
}
```
