# 간격 체계

기본 단위에 따른 척도로 간격을 일관되게 관리한다.

## AppSpacing

```dart
const double spacingSpaceUnit = 16;

/// 4px
const double spacingXxs = 0.25 * spacingSpaceUnit;

/// 6px
const double spacingXs = 0.375 * spacingSpaceUnit;

/// 8px
const double spacingSm = 0.5 * spacingSpaceUnit;

/// 12px
const double spacingMd = 0.75 * spacingSpaceUnit;

/// 16px
const double spacingLg = spacingSpaceUnit;

/// 24px
const double spacingXlg = 1.5 * spacingSpaceUnit;

/// 32px
const double spacingXxlg = 2 * spacingSpaceUnit;
```

## 적용 예제

```dart
Padding(
  padding: EdgeInsets.symmetric(
    horizontal: spacingLg,
    vertical: spacingMd,
  ),
  child: Column(
    spacing: spacingSm,
    children: [
      // 위젯
    ],
  ),
)
```

## 명명된 인수 사용

`EdgeInsets.only`를 사용한다.

```dart
// 권장: 값이 적용되는 방향이 명확하다.
EdgeInsets.only(top: 16, bottom: 8)
```

대칭이면 `EdgeInsets.symmetric`을 사용한다.

```dart
// 권장: 가로·세로 값이 같을 때 간결하다.
EdgeInsets.symmetric(horizontal: 16, vertical: 8)
```

위치 인수가 많은 `EdgeInsets.fromLTRB`는 피한다.

```dart
// 피할 패턴: 위치 인수는 방향을 혼동하기 쉽다.
EdgeInsets.fromLTRB(16, 8, 16, 8)
```
