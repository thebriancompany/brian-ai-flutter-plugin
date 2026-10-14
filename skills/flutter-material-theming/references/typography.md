# 서체

## 폰트 에셋

`assets/fonts/`에 저장하고 `pubspec.yaml`에 등록한다.

```yaml
flutter:
  fonts:
    - family: Inter
      fonts:
        - asset: assets/fonts/Inter-Regular.ttf
          weight: 400
        - asset: assets/fonts/Inter-Medium.ttf
          weight: 500
        - asset: assets/fonts/Inter-Bold.ttf
          weight: 700
```

`flutter_gen`으로 타입 안전한 폰트 상수를 생성할 수 있다.

```dart
const String fontFamilyInter = 'Inter';
```

## 공통 텍스트 스타일

일관된 변경을 위해 테마 모듈의 최상위 선언에 모은다.

```dart
const _baseStyle = TextStyle(
  fontFamily: fontFamilyInter,
  fontWeight: FontWeight.w400,
);

final TextStyle appDisplayLarge = _baseStyle.copyWith(
  fontSize: 57,
  height: 1.12,
  fontWeight: FontWeight.w400,
);

final TextStyle appHeadlineMedium = _baseStyle.copyWith(
  fontSize: 28,
  height: 1.29,
  fontWeight: FontWeight.w400,
);

final TextStyle appTitleLarge = _baseStyle.copyWith(
  fontSize: 20,
  height: 1.3,
  fontWeight: FontWeight.w500,
);

final TextStyle appBodyLarge = _baseStyle.copyWith(
  fontSize: 16,
  height: 1.5,
  fontWeight: FontWeight.w400,
);

final TextStyle appLabelLarge = _baseStyle.copyWith(
  fontSize: 14,
  height: 1.43,
  fontWeight: FontWeight.w500,
);
```

## TextTheme 연결

`ThemeData.textTheme`에 등록한다.

```dart
ThemeData(
  textTheme: TextTheme(
    displayLarge: appDisplayLarge,
    headlineMedium: appHeadlineMedium,
    titleLarge: appTitleLarge,
    bodyLarge: appBodyLarge,
    labelLarge: appLabelLarge,
  ),
)
```

## 위젯에서 읽기

```dart
@override
Widget build(BuildContext context) {
  final textTheme = Theme.of(context).textTheme;

  return Text('Hello', style: textTheme.headlineMedium);
}
```
