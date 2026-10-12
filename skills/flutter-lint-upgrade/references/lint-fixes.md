# 린트 수정 참고

## 일반적인 규칙

| 규칙 | 수정 | 주의 |
| --- | --- | --- |
| `prefer_const_constructors` | 가능한 생성에 const 추가 | 객체 정체성 등 문맥 확인 |
| `use_super_parameters` | 명시적 전달을 super 매개변수로 단순화 | 기존 의미 유지 |
| `unnecessary_late` | 불필요한 late 제거 | 초기화 시점이 바뀌지 않는지 확인 |
| `avoid_dynamic_calls` | 구체적 타입·검증된 변환 사용 | 캐스팅으로 TypeError가 생길 수 있음 |
| `require_trailing_commas` | 쉼표 추가 | 포맷 규칙 확인 |
| `unnecessary_null_checks` | 불필요한 ! 제거 | 분석 결과에 근거 |

예를 들어 JSON 정수에 `as double`을 추가하면 원래 동작하던 숫자 연산이 실패할 수 있다. 단순 스타일 수정으로 간주하지 않는다.

## Dart 3.13 생성자 규칙

프로젝트 SDK와 설치한 린트 버전이 실제로 지원하는지 확인한다. 낮은 SDK에 새 문법을 적용하지 않는다.

- `unnecessary_type_name_in_constructor`: 클래스 본문의 이름 없는 생성자를 `new`로 표현한다. 반드시 기본 생성자 형태 전체로 바꿀 필요는 없다.
- `use_declaring_parameters`: 이미 기본 생성자인 경우 `this.field`를 `final Type field` 같은 선언 매개변수로 바꾼다.
- `unnecessary_primary_constructor_body`: 빈 기본 생성자 본문을 세미콜론으로 대체한다.
- `empty_container_bodies`: 지원되는 빈 클래스·믹스인·확장 타입 본문을 세미콜론으로 대체한다.

최소 수정:

```dart
// 수정 전: Dart 3.13 이상의 unnecessary_type_name_in_constructor 진단
class ProfileCard extends StatelessWidget {
  const ProfileCard({required this.userId, super.key});

  final String userId;

  @override
  Widget build(BuildContext context) => Text(userId);
}

// 최소 수정: 이름 없는 생성자를 new로 선언
class ProfileCard extends StatelessWidget {
  const new({required this.userId, super.key});

  final String userId;

  @override
  Widget build(BuildContext context) => Text(userId);
}
```

추가 현대화가 범위에 포함된 경우:

```dart
// 현대화: 선언 매개변수를 가진 기본 생성자
class const ProfileCard({required final String userId, super.key})
    extends StatelessWidget {
  @override
  Widget build(BuildContext context) => Text(userId);
}
```

`const` 위치와 상속 절을 확인한다. SDK 갱신이 별도로 필요하면 사용자 요청 범위와 호환성을 검토하고 수행한다.
