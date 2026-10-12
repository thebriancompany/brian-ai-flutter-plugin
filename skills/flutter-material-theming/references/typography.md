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
class FontFamily {
  static const String inter = 'Inter';
}
```

## 공통 텍스트 스타일

일관된 변경을 위해 한 클래스에 모은다.

```dart
abstract class AppTextStyle {
  static const _baseStyle = TextStyle(
    fontFamily: FontFamily.inter,
    fontWeight: FontWeight.w400,
  );

  static final TextStyle displayLarge = _baseStyle.copyWith(
    fontSize: 57,
    height: 1.12,
    fontWeight: FontWeight.w400,
  );

  static final TextStyle headlineMedium = _baseStyle.copyWith(
    fontSize: 28,
    height: 1.29,
    fontWeight: FontWeight.w400,
  );

  static final TextStyle titleLarge = _baseStyle.copyWith(
    fontSize: 20,
    height: 1.3,
    fontWeight: FontWeight.w500,
  );

  static final TextStyle bodyLarge = _baseStyle.copyWith(
    fontSize: 16,
    height: 1.5,
    fontWeight: FontWeight.w400,
  );

  static final TextStyle labelLarge = _baseStyle.copyWith(
    fontSize: 14,
    height: 1.43,
    fontWeight: FontWeight.w500,
  );
}
```

## TextTheme 연결

`ThemeData.textTheme`에 등록한다.

```dart
ThemeData(
  textTheme: TextTheme(
    displayLarge: AppTextStyle.displayLarge,
    headlineMedium: AppTextStyle.headlineMedium,
    titleLarge: AppTextStyle.titleLarge,
    bodyLarge: AppTextStyle.bodyLarge,
    labelLarge: AppTextStyle.labelLarge,
  ),
)
```

## 위젯에서 읽기

```dart
@override
Widget build(BuildContext context) {
  final textTheme = Theme.of(context).textTheme;

  return Text(
    'Hello',
    style: textTheme.headlineMedium,
  );
}
```
