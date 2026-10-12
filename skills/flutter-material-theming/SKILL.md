---
name: flutter-material-theming
description: "Flutter ThemeData·ColorScheme·TextTheme, 컴포넌트 스타일, 간격과 다크 모드를 구현하거나 하드코딩된 위젯 스타일을 정리할 때 사용한다."
---

# Material 테마

색상·서체·컴포넌트 스타일은 `ThemeData`를 기준으로 일관되게 관리한다.

## 핵심 기준

- 위젯에서 색상·텍스트 스타일을 직접 정의하지 않는다. 색은 `Theme.of(context).colorScheme`, 글자는 `Theme.of(context).textTheme`에서 읽는다.
- `FilledButtonThemeData`, `InputDecorationTheme` 같은 컴포넌트 테마를 `ThemeData`에 모은다. 공통 장식 헬퍼나 래퍼로 중복을 옮기기만 하지 않는다.
- 기본 단위에 따른 간격 척도를 사용한다. 임의의 패딩·마진·간격을 흩어 놓지 않는다.
- 밝은 테마와 어두운 테마를 함께 정의한다. 위젯의 밝기 분기 대신 각 테마의 같은 색상 역할을 읽는다.
- 위치 인수인 `EdgeInsets.fromLTRB`보다 `only`·`symmetric`을 사용한다. RTL 대응이 필요하면 방향 기반 API를 쓴다.
- 기존 디자인 시스템과 사용자의 요구를 우선한다. 테마 전환이 필요한 부분만 수정하고 관련 없는 스타일을 재설계하지 않는다.

## 색상

모든 색상 정의를 별도 클래스에 모은다.

```dart
abstract class AppColors {
  static const primaryColor = Color(0xFF4F46E5);
  static const secondaryColor = Color(0xFF9C27B0);
  static const errorColor = Color(0xFFDC2626);
  static const surfaceColor = Color(0xFFFAFAFA);
}
```

밝은·어두운 `ColorScheme`을 `AppTheme`에서 구성하고 `MaterialApp`의 `theme`, `darkTheme`에 전달한다.

```dart
class AppTheme {
  static ThemeData get light => ThemeData(
    colorScheme: const ColorScheme.light(
      brightness: Brightness.light,
      surface: AppColors.surfaceColor,
      // 나머지 색상 역할
    ),
  );

  static ThemeData get dark => ThemeData(
    colorScheme: const ColorScheme.dark(
      brightness: Brightness.dark,
      surface: AppColors.surfaceColorDark,
      // 나머지 색상 역할
    ),
  );
}
```

[색상 역할과 시드 생성](references/color-scheme.md)을 참고한다.

## 서체

기본 스타일과 `displayLarge`, `headlineMedium`, `bodyLarge` 등의 변형을 `AppTextStyle`에 정의하고 `TextTheme`에 등록한다. [폰트 등록과 전체 예제](references/typography.md)를 참고한다.

직접 지정한 글자 크기·굵기는 앱에 등록된 가장 가까운 슬롯으로 옮긴다. 예를 들어 18/w500은 앱의 `titleLarge`, 16/w400은 `bodyLarge`, 14/w500은 `labelLarge`를 검토한다. 실제 디자인에 맞춰 중앙 정의를 조정한다. 등록하지 않은 슬롯은 Material 기본 글꼴로 돌아갈 수 있다. 호출 지점의 `copyWith`는 색상 역할처럼 문맥에 필요한 값에 한정한다.

```dart
final theme = Theme.of(context);

Text(
  label,
  style: theme.textTheme.titleLarge?.copyWith(
    color: theme.colorScheme.onPrimary,
  ),
)
```

색상만 옮기고 위젯의 `TextStyle(fontSize: ..., fontWeight: ...)`를 남기면 서체 중앙화가 끝난 것이 아니다.

## 컴포넌트 테마

버튼·입력 필드·앱 바 스타일을 `ThemeData`에 모은다. [컴포넌트별 구성과 전체 조립](references/components.md)을 참고한다.

여러 필드에 같은 장식이 반복되면 해당 테마로 옮기고 호출 지점에서는 삭제한다. 모든 호출부가 별도 래퍼를 선택해야 하는 구조보다 기본 Material 위젯에도 적용되는 테마를 우선한다.

```dart
// 올바른 예: 기본 스타일을 테마에 둔다.
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

필드는 고유한 내용만 선언한다.

```dart
TextFormField(
  decoration: const InputDecoration(labelText: 'Email'),
)
```

## 간격 체계

`AppSpacing`의 기본 단위와 배수로 `xxs`부터 `xxlg`까지 정의한다. 규칙을 제안할 때는 실제 클래스도 제공한다.

```dart
abstract class AppSpacing {
  static const double spaceUnit = 16;

  static const double xxs = 0.25 * spaceUnit; // 4
  static const double sm = 0.5 * spaceUnit; // 8
  static const double md = 0.75 * spaceUnit; // 12
  static const double lg = spaceUnit; // 16
  static const double xxlg = 2 * spaceUnit; // 32
}
```

[간격 사용 예제](references/spacing.md)를 참고한다.

## 테마 생성 순서

1. `AppColors`, `AppTextStyle`, `AppSpacing`을 정의한다.
2. `AppTheme`에 `light`·`dark`를 만든다.
3. 각각의 `ThemeData`에 색상·서체·컴포넌트 테마를 연결한다.
4. 두 테마를 `MaterialApp`에 전달한다.

위젯의 밝기 조건은 두 테마에서 같은 `ColorScheme` 역할에 각 색을 지정하는 방식으로 옮긴다. 위젯에서는 조건 없이 역할을 읽는다.

```dart
@override
Widget build(BuildContext context) {
  return ColoredBox(
    color: Theme.of(context).colorScheme.surface,
    child: child,
  );
}
```

## 참고 문서

- [ColorScheme](references/color-scheme.md)
- [서체](references/typography.md)
- [컴포넌트](references/components.md)
- [간격](references/spacing.md)
