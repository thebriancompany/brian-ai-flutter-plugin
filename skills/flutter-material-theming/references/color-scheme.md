# ColorScheme 구성

Material 3 색상 역할을 `ThemeData` 안에서 구성한다. 사용 가능한 역할은 프로젝트 Flutter 버전에 맞춘다.

```dart
ThemeData(
  colorScheme: ColorScheme(
    brightness: Brightness.light,
    primary: brandPrimaryColor,
    secondary: brandSecondaryColor,
    error: brandErrorColor,
    surface: brandSurfaceColor,
    onPrimary: Colors.white,
    onSecondary: Colors.white,
    onError: Colors.white,
    onSurface: Colors.black,
  ),
)
```

`ColorScheme.fromSeed()`는 실제 제품에서도 사용할 수 있는 Material 3 구성 방식이다. 브랜드 요구에 맞춰 역할을 조정하고 실제 대비를 검증한다.

```dart
ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: brandPrimaryColor,
  ),
)
```

## 밝은 테마와 어두운 테마

같은 테마 모듈에서 두 색상 구성을 만든다.

```dart
ThemeData get lightTheme =>
    ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: brandPrimaryColor));

ThemeData get darkTheme => ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: brandPrimaryColor,
    brightness: Brightness.dark,
  ),
);
```

`MaterialApp`의 `theme`·`darkTheme`에 각각 전달한다.

## 위젯에서 색상 읽기

```dart
@override
Widget build(BuildContext context) {
  final colorScheme = Theme.of(context).colorScheme;

  return ColoredBox(
    color: colorScheme.surface,
    child: Text('Hello', style: TextStyle(color: colorScheme.onSurface)),
  );
}
```
