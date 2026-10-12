# 텍스트 방향

## Directionality

지역화가 현재 방향을 결정하며 필요한 범위에서 명시적으로 재정의할 수 있다.

```dart
Directionality(
  textDirection: TextDirection.rtl,
  child: Row(
    children: [
      // 자식을 오른쪽에서 왼쪽으로 배치한다.
    ],
  ),
)
```

현재 방향은 `Directionality.of(context)`로 읽는다.

| 방식 | 기준 | 용도 |
| --- | --- | --- |
| 절대 방향 | top·left·right·bottom | 문자 방향과 무관한 위치 |
| 상대 방향 | top·start·end·bottom | RTL을 따르는 배치 |

## 방향 기반 여백

읽기 방향을 따라야 하는 여백은 `EdgeInsetsDirectional`을 사용한다.

```dart
// 권장: RTL 반영
Padding(
  padding: EdgeInsetsDirectional.only(start: 12),
  child: Text('Padding at text start regardless of direction'),
)

// 문자 방향과 무관한 절대 배치에만 사용한다.
Padding(
  padding: EdgeInsets.only(left: 10),
  child: Text('Always 10px from left edge'),
)
```

위치는 `PositionedDirectional`, 정렬은 `Align(alignment: AlignmentDirectional...)`, 테두리는 `BorderDirectional`을 사용한다.

## 아이콘과 이미지

방향성이 있는 Material 아이콘은 `IconData.matchTextDirection`을 통해 반전된다. 모든 아이콘이 자동으로 반전되는 것은 아니다. 반전을 막아야 하면 `Icon.textDirection`을 명시한다. 이미지는 기본적으로 반전되지 않으므로 필요할 때 `Image.matchTextDirection: true`를 지정한다.

`Icon` 생성자에는 `matchTextDirection`이 없다. 그것은 IconData의 필드이며 Image의 매개변수다.

```dart
// 방향성 IconData는 자체 반전하고 이미지는 설정이 필요하다.
Row(
  children: [
    const Icon(Icons.arrow_forward),
    const Image(
      image: AssetImage('assets/swipe_hint.png'),
      matchTextDirection: true,
    ),
  ],
)
```

진행·미래 방향의 화살표는 반전한다. 미디어 진행 표시, 부정 기호, 시계·도구 같은 물리적 대상은 보통 반전하지 않는다.
