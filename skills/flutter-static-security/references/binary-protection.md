# 바이너리와 설정 보호

## Dart 난독화

릴리스 정책에 맞춰 적용하고 심볼 파일은 오류 분석을 위해 보관한다. 난독화는 비밀을 숨기는 보안 경계가 아니다.

```bash
flutter build apk --obfuscate --split-debug-info=build/symbols/
flutter build ipa --obfuscate --split-debug-info=build/symbols/
```

## Android 백업

대상 OS·SDK와 저장소 라이브러리 문서를 확인해 `allowBackup`, 백업 제외 규칙과 데이터 전송 규칙을 함께 점검한다. 단일 플래그만으로 모든 OS·제조사의 전송 동작이 차단된다고 주장하지 않는다.

```xml
<!-- AndroidManifest.xml -->
<!-- ❌ Default — allows ADB backup of app data -->
<application android:allowBackup="true" ...>

<!-- ✅ Disable backup for apps storing sensitive data -->
<application android:allowBackup="false" ...>
```

## 런타임 무결성

`freerasp` 같은 도구는 루팅·탈옥·디버거·재패키징 탐지에 쓰인다. 정적 검토 범위 밖이며 서버 측 통제와 위협 모델을 대체하지 않는다.
