---
name: flutter-material-theming
description: "Flutter ThemeData·ColorScheme·TextTheme, 컴포넌트 스타일, 간격과 다크 모드를 구현하거나 하드코딩된 위젯 스타일을 정리할 때 사용한다."
---

# Material 테마

색상·서체·컴포넌트 스타일은 `ThemeData`를 기준으로 일관되게 관리한다.

공식 권고와 팀 관례의 구분, SDK·언어 버전, 오류·수명 처리는 [공통 기준](../flutter-review/SKILL.md#공식-기준과-프로젝트-관례)을 적용한다.

## 핵심 기준

- 공통 색상·텍스트 스타일은 테마에 둔다. 한 화면의 의도적인 변형에는 로컬 Theme·copyWith도 사용할 수 있다. 색은 `Theme.of(context).colorScheme`, 글자는 `Theme.of(context).textTheme`에서 읽는다.
- `FilledButtonThemeData`, `InputDecorationThemeData` 같은 컴포넌트 테마를 `ThemeData`에 모은다. 공통 장식 헬퍼나 래퍼로 중복을 옮기기만 하지 않는다.
- 기본 단위에 따른 간격 척도를 사용한다. 임의의 패딩·마진·간격을 흩어 놓지 않는다.
- 제품이 다크 모드를 지원하면 밝은 테마와 어두운 테마를 함께 정의한다. 위젯의 밝기 분기 대신 각 테마의 같은 색상 역할을 읽는다.
- 위치 인수인 `EdgeInsets.fromLTRB`보다 `only`·`symmetric`을 사용한다. RTL 대응이 필요하면 방향 기반 API를 쓴다.
- 기존 디자인 시스템과 사용자의 요구를 우선한다. 테마 전환이 필요한 부분만 수정하고 관련 없는 스타일을 재설계하지 않는다.

## 색상

색상은 테마 정의에 모은다. 단순 토큰은 최상위 상수로 선언하고, 테마마다 달라지는 추가 역할은 ThemeExtension으로 표현한다.

```dart
const brandPrimaryColor = Color(0xFF4F46E5);
const brandSecondaryColor = Color(0xFF9C27B0);
const brandErrorColor = Color(0xFFDC2626);
const brandSurfaceColor = Color(0xFFFAFAFA);
const brandSurfaceColorDark = Color(0xFF121212);
```

밝은·어두운 `ColorScheme`을 테마 팩토리에서 구성하고 `MaterialApp`의 `theme`, `darkTheme`에 전달한다.

```dart
ThemeData get lightTheme => ThemeData(
  colorScheme: const ColorScheme.light(
    brightness: Brightness.light,
    surface: brandSurfaceColor,
    // 나머지 색상 역할
  ),
);

ThemeData get darkTheme => ThemeData(
  colorScheme: const ColorScheme.dark(
    brightness: Brightness.dark,
    surface: brandSurfaceColorDark,
    // 나머지 색상 역할
  ),
);
```

[색상 역할과 시드 생성](references/color-scheme.md)을 참고한다.

## 서체

기본 스타일과 `displayLarge`, `headlineMedium`, `bodyLarge` 등의 변형을 최상위 선언으로 정의하고 `TextTheme`에 등록한다. [폰트 등록과 전체 예제](references/typography.md)를 참고한다.

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

필드는 고유한 내용만 선언한다.

```dart
TextFormField(
  decoration: const InputDecoration(labelText: 'Email'),
)
```

## 간격 체계

간격의 기본 단위와 배수를 최상위 상수로 정의한다. 기존 디자인 토큰이 있으면 그 API를 유지한다.

```dart
const double spacingSpaceUnit = 16;

const double spacingXxs = 0.25 * spacingSpaceUnit; // 4
const double spacingSm = 0.5 * spacingSpaceUnit; // 8
const double spacingMd = 0.75 * spacingSpaceUnit; // 12
const double spacingLg = spacingSpaceUnit; // 16
const double spacingXxlg = 2 * spacingSpaceUnit; // 32
```

[간격 사용 예제](references/spacing.md)를 참고한다.

## 테마 생성 순서

1. 재사용할 색상·서체·간격 토큰을 정의한다.
2. `lightTheme`·`darkTheme`를 만든다.
3. 각각의 `ThemeData`에 색상·서체·컴포넌트 테마를 연결한다.
4. 두 테마를 `MaterialApp`에 전달한다.

위젯의 밝기 조건은 두 테마에서 같은 `ColorScheme` 역할에 각 색을 지정하는 방식으로 옮긴다. 위젯에서는 조건 없이 역할을 읽는다.

```dart
@override
Widget build(BuildContext context) {
  return ColoredBox(color: Theme.of(context).colorScheme.surface, child: child);
}
```

## 참고 문서

- [ColorScheme](references/color-scheme.md)
- [서체](references/typography.md)
- [컴포넌트](references/components.md)
- [간격](references/spacing.md)
