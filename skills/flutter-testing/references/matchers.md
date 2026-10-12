# 매처 빠른 참조

| 매처 | 검증 |
| --- | --- |
| `equals(x)` | 깊은 동등성 |
| `isA<T>()` | 타입 |
| `isA<T>().having(fn, name, matcher)` | 타입과 속성 |
| `isNull` / `isNotNull` | null 여부 |
| `isTrue` / `isFalse` | 불리언 |
| `contains(x)` | 컬렉션·문자열 포함 |
| `hasLength(n)` | 원소 수 |
| `isEmpty` / `isNotEmpty` | 비어 있는지 |
| `predicate<T>(fn)` | 사용자 정의 불리언 조건 |
| `closeTo(value, delta)` | 오차 범위 |
| `greaterThan(n)` / `lessThan(n)` | 수치 비교 |
| `containsAll(list)` | 모든 원소 포함 |
| `containsAllInOrder(list)` | 순서대로 포함 |
| `throwsA(matcher)` | 일치하는 예외 |
| `throwsA(isA<T>())` | 특정 타입 예외 |
| `emits(matcher)` | 스트림 값 |
| `emitsInOrder(list)` | 스트림 순서 |
| `emitsDone` | 스트림 종료 |
| `emitsError(matcher)` | 스트림 오류 |
| `neverEmits(matcher)` | 해당 값 방출하지 않음 |
