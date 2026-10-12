# 백엔드 연동

## 다국어 콘텐츠

1. 지원 언어별 번역을 저장한다.
2. 요청 또는 세션 초기화 시 사용자의 locale을 받는다.
3. 요청한 언어로 콘텐츠를 반환한다.

## 오류 지역화

HTTP 상태 코드를 지역화 키로 매핑하거나, 백엔드가 반환한 안정적인 오류 상수를 변환한다.

```dart
// 백엔드 반환 예: { "error": "expired_code" }
// 프런트엔드에서 지역화 키로 변환한다.
final message = switch (error) {
  'invalid_code' => context.l10n.errorInvalidCode,
  'expired_code' => context.l10n.errorExpiredCode,
  'limit_reached' => context.l10n.errorLimitReached,
  _ => context.l10n.errorGeneric,
};
```
