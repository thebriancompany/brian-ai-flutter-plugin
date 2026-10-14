---
name: flutter-static-security
description: "Flutter/Dart의 비밀값, 민감 정보, 인증, 네트워크, 암호와 의존성을 정적으로 검토하거나 관련 코드를 수정할 때 사용한다."
---

# Flutter 정적 보안 검토

Flutter/Dart 소스에서 비밀값·저장소·네트워크·인증·암호·로그·의존성 문제를 검토한다. [OWASP Mobile Top 10](https://owasp.org/www-project-mobile-top-10/)을 참고하며 침투 테스트나 실제 런타임 안전성 검증을 수행했다고 주장하지 않는다.

공식 권고와 팀 관례의 구분, SDK·언어 버전, 오류·수명 처리는 [공통 기준](../flutter-review/SKILL.md#공식-기준과-프로젝트-관례)을 적용한다.

## 핵심 기준

- 앱에 배포된 값은 추출될 수 있다. 비공개 서버 자격 증명을 소스·설정·에셋에 넣지 않는다.
- `--dart-define`, `String.fromEnvironment`, `.env`, 난독화, 문자열 분할은 비밀 보호 수단이 아니다. 서버가 비밀을 보관하고 권한이 제한된 요청을 처리하게 한다.
- 민감한 로컬 값은 플랫폼 보호 저장소를 사용한다. `SharedPreferences`에는 테마·언어 등 민감하지 않은 설정만 둔다.
- HTTPS와 정상 인증서 검증을 사용한다. 개발용 예외가 배포 설정에 들어가지 않게 한다.
- 보안용 난수는 `Random.secure()`를 쓴다. 검증된 암호 구현을 사용하고 직접 설계하지 않는다.
- 인증·권한은 서버에서 매 요청 검증한다. 저장소의 토큰 처리나 위젯·라우트 조건만으로 서버 권한 검증을 대체하지 않는다.
- 로그에 토큰·비밀번호·개인정보·인증 헤더를 남기지 않는다.
- 의존성 검토 시 해결된 `pubspec.lock`과 보안 권고를 확인한다. 릴리스 보안 검토에서는 OSV 같은 스캐너의 실제 결과를 사용한다.
- Android 백업 정책은 OS·대상 SDK·저장소 라이브러리 설정을 함께 검토한다.
- 문제에는 `Critical`, `Warning`, `Note`와 위치·영향·개선안을 붙인다. 보안성이 확인되지 않은 패키지나 설정을 단순히 점수가 낮다는 이유로 취약하다고 단정하지 않는다.

## 심각도

| 수준 | 예 |
| --- | --- |
| `Critical` | 실제 비밀키 노출, 인증서 검증 우회, 평문 세션 토큰, 민감 로그 |
| `Warning` | 보안 목적의 약한 난수, 부적절한 백업, 검증 누락, 설명 없는 권고 무시 |
| `Note` | 난독화 고려, 업데이트 검토, 의존성 고정 정책 검토 |

환경·악용 가능성에 따라 판단한다. 인증서 고정이나 특정 폼 라이브러리를 쓰지 않는 사실만으로 결함을 확정하지 않는다.

## 비밀값과 API 키

Dart, `.env`, 네이티브 설정, `google-services.json`, plist·manifest를 점검한다. 공개 클라이언트 식별자와 실제 비공개 자격 증명을 구분한다.

```dart
// ❌ 바이너리에서 추출할 수 있는 하드코딩된 비밀키
const apiKey = 'sk-abc123';

// ❌ 빌드 시 주입: dart-define도 값을 클라이언트에 포함하므로
// 추출 가능성을 없애지 않는다.
const injectedKey = String.fromEnvironment('API_KEY');

// 공개 식별용 Firebase API 키는 존재만으로 비밀 유출이 아니다.
// 실제 서비스 권한·API 제한·Security Rules를 별도로 확인한다.
```

Firebase 클라이언트 API 키와 Mapbox 공개 토큰은 용도·권한·제한 설정으로 판단한다. [Firebase 키 안내](https://firebase.google.com/docs/projects/api-keys)를 참고하고 서버 비밀과 혼동하지 않는다.

다음은 런타임 자격 증명 흐름의 예제다. 서버의 장기 비밀을 그대로 내려주는 설계는 해결책이 아니다. 사용자별 단기 토큰 또는 서버 프록시로 대체한다.

```dart
// 서버 런타임 흐름 예: 장기 비밀 대신 사용자별 단기 토큰을 사용한다.
final accessToken = await authService.fetchShortLivedAccessToken();
```

| 이동 방법 | 해결되지 않는 이유 |
| --- | --- |
| dart-define·String.fromEnvironment | 값이 클라이언트에 포함됨 |
| 에셋 .env | 번들에서 읽을 수 있음 |
| 네이티브 설정 파일 | 앱과 함께 배포됨 |
| 난독화·문자열 분할 | 추출 비용만 높임 |
| kReleaseMode 분기 | 배포 분기에 여전히 값이 존재 |

CI 비밀 저장소는 앱에 포함되지 않는 서명·배포 자격 증명에 적합하다. 실제 자격 증명을 저장소에 커밋하지 않는다.

## 로컬 저장

`flutter_secure_storage` 등의 플랫폼 보호 기능을 사용하고 대상 OS의 보장 범위를 확인한다. 모든 기기에서 하드웨어 보호가 동일하다고 가정하지 않는다.

```dart
// ❌ SharedPreferences에 암호화 없이 저장한 JWT
final prefs = await SharedPreferences.getInstance();
prefs.setString('auth_token', jwt);

// ❌ 암호화하지 않은 로컬 파일의 민감한 값
await File('${dir.path}/user.json').writeAsString(jsonEncode(user));
```

```dart
// ✅ 플랫폼 보호 저장소를 사용하는 flutter_secure_storage
const storage = FlutterSecureStorage();
await storage.write(key: 'auth_token', value: jwt);
final token = await storage.read(key: 'auth_token');
await storage.delete(key: 'auth_token');
```

## 네트워크

평문 HTTP와 인증서 검증 우회를 확인한다.

```dart
// ❌ 평문 HTTP 주소
final dio = Dio(BaseOptions(baseUrl: 'http://api.example.com'));

// ❌ 인증서 검증 해제로 중간자 공격에 노출
final client = HttpClient()
  ..badCertificateCallback = (cert, host, port) => true;
```

```dart
// ✅ HTTPS 주소
final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));
```

인증서 고정은 위협 모델과 인증서 회전·복구 계획이 있는 경우 검토한다. 기본 TLS 검증을 유지한다. [암호와 인증](references/crypto.md)을 참고한다.

## 인증

서버가 요청마다 토큰과 권한을 확인해야 한다. 민감한 앱 흐름의 생체 인증은 `local_auth` 같은 검증된 플랫폼 추상화를 사용한다.

```dart
import 'package:local_auth/local_auth.dart';

class BiometricGate {
  BiometricGate({LocalAuthentication? auth})
    : _auth = auth ?? LocalAuthentication();

  final LocalAuthentication _auth;

  Future<bool> authenticate() async {
    try {
      if (!await _auth.canCheckBiometrics) return false;

      return await _auth.authenticate(
        localizedReason: 'Confirm your identity to continue to payments',
        biometricOnly: true,
      );
    } on LocalAuthException {
      // 등록된 생체 정보가 없거나 실패가 누적되면 접근을 허용하지 않는다.
      return false;
    }
  }
}
```

이 예제는 [local_auth 3.x](https://pub.dev/packages/local_auth/changelog)의 직접 옵션·LocalAuthException API다. 2.x 프로젝트는 해당 버전의 AuthenticationOptions·PlatformException을 유지하고 예제 때문에 업그레이드하지 않는다. 인증 안내 문구는 앱 지역화에서 전달한다.

생체 인증은 로컬 접근 제어이며 결제 등 서버 권한 확인을 대신하지 않는다. 기존 인증 제공자와 인증 설계를 존중한다.

## 암호

검증된 패키지·알고리즘을 사용한다.

```dart
// ❌ 보안 목적에 부적합한 dart:math Random
import 'dart:math';
final sessionId = Random().nextInt(1 << 32).toRadixString(16);
final iv = List.generate(16, (_) => Random().nextInt(256));

// ❌ 보안 용도로 부적합한 MD5·SHA-1
import 'dart:convert';
final hash = md5.convert(utf8.encode(password)).toString();

// ❌ 하드코딩한 암호 키
const encryptionKey = 'my-secret-key-123';
```

```dart
// ✅ 보안용 Random.secure()로 최소 16바이트(128비트)를 생성한다.
import 'dart:convert';
import 'dart:math';

import 'package:crypto/crypto.dart';

final secureRandom = Random.secure();
final sessionBytes = List<int>.generate(16, (_) => secureRandom.nextInt(256));
final sessionId = base64UrlEncode(sessionBytes);
final iv = List<int>.generate(16, (_) => secureRandom.nextInt(256));

// ✅ 표준 해시: 비밀번호 저장용 해시와 구분한다.
final hash = sha256.convert(utf8.encode(data)).toString();

// ✅ 소스 코드가 아닌 보호 저장소에서 얻은 키
final key = await storage.read(key: 'encryption_key');
```

세션 식별자는 `Random.secure()` 사용 여부와 별개로 최소 16바이트의 난수를 채워 hex 또는 base64url로 인코딩한다. 32비트 정수 하나는 가능한 값이 `2^32`개뿐이며 인코딩해도 출력 공간이 늘어나지 않는다. 인증 세션은 서버에서 발급·검증한다. IV 길이와 유일성 요건은 사용하는 암호 알고리즘을 따른다.

보안 용도로 MD5·SHA-1·DES·RC4·ECB를 피한다. 일반 해시와 비밀번호 저장 해시를 구분한다. 새 서버 비밀번호 저장에는 OWASP의 최신 지침을 확인하고 Argon2id 같은 적응형 해시를 검토한다. 빠른 SHA-256을 비밀번호 저장용으로 사용하지 않는다.

## 입력 검증

클라이언트 검증은 사용자 피드백을 위한 것이며 서버 검증·권한·쿼리 매개변수화도 필요하다.

```dart
// ❌ 검증하지 않은 컨트롤러 문자열을 API에 직접 전달
ElevatedButton(
  onPressed: () => context.read<AuthBloc>().add(
    LoginRequested(
      email: _emailController.text,
      password: _passwordController.text,
    ),
  ),
  child: const Text('Login'),
);
```

```dart
// ✅ 검증한 FormzInput 값을 상태에 유지
import 'package:formz/formz.dart';

enum EmailValidationError { empty, invalid }

class Email extends FormzInput<String, EmailValidationError> {
  const Email.pure() : super.pure('');
  const Email.dirty([super.value = '']) : super.dirty();

  @override
  EmailValidationError? validator(String value) {
    final emailRegex = RegExp(r'^[^@]+@[^@]+\.[^@]+$');
    if (value.isEmpty) return EmailValidationError.empty;
    if (!emailRegex.hasMatch(value)) return EmailValidationError.invalid;
    return null;
  }
}
```

```dart
// ✅ 위젯 제출은 유효성을 확인하고 컨트롤러가 아닌
// 상태의 검증된 값을 사용한다.
ElevatedButton(
  onPressed: state.isValid
      ? () => context.read<AuthBloc>().add(
            LoginRequested(
              email: state.email.value,
              password: state.password.value,
            ),
          )
      : null,
  child: const Text('Login'),
);
```

`formz` 패턴에서는 필드별 `FormzInput`과 길이·형식 규칙을 두고 onChanged에서 Bloc 상태를 갱신한다. 제출은 검증된 상태를 사용한다. 기존 프로젝트의 동등한 검증 방식도 존중한다.

## 로그

로그는 디버깅·오류 수집 도구에 노출될 수 있다.

```dart
// ❌ 로그에 포함된 토큰
debugPrint('Auth token: $token');
log('User data: ${jsonEncode(user)}');
print('Request headers: $headers'); // 헤더에 Bearer 토큰이 포함될 수 있다.

// ❌ 예외 내부 정보를 UI에 그대로 노출
catch (e) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text(e.toString())), // 스택 추적이나 SQL이 포함될 수 있다.
  );
}
```

```dart
// ✅ 민감하지 않은 식별자만 기록
debugPrint('Login attempt started'); // 사용자 식별자도 개인정보일 수 있다.

// ✅ UI에 보여 줄 오류 메시지 정제
on AuthException catch (e, stackTrace) {
  reportSanitizedAuthFailure(e, stackTrace); // 앱의 민감 정보 제거 헬퍼
  emit(state.copyWith(status: LoginStatus.failure)); // UI에는 일반 오류 메시지 표시
}
```

전체 사용자 객체·Authorization 헤더·토큰·비밀번호·개인정보를 제거하거나 필요한 비민감 정보만 남긴다.

## 의존성

직접 목록만으로 결론 내리지 않고 해결된 간접 의존성도 확인한다. 아래 실행 예제는 설치된 도구 버전의 `--help`와 대조한다.

```bash
dart pub get                        # 의존성 해결 중 보안 권고 확인
osv-scanner --lockfile=pubspec.lock # 해결된 간접 의존성을 OSV와 비교
dart pub outdated                   # 사용 가능한 업데이트 확인
```

`ignored_advisories`에는 각 항목을 무시하는 구체적인 근거를 같은 파일에 기록한다.

```yaml
ignored_advisories:
  - GHSA-4rgh-jx4f-xxxx # 예시 무시 사유는 실제 취약 코드 경로·배포 조건으로 검증할 것
```

근거 없는 무시는 Warning으로 보고하고, 버전 고정은 자동 패치 갱신을 막을 수 있으므로 프로젝트 정책에 따라 Note로 검토한다. 스캔 실패·미실행·오래된 결과를 취약점 없음으로 표현하지 않는다.

## 참고 문서

- [공급망](references/supply-chain.md): 패키지 출처·권한·OSV
- [바이너리](references/binary-protection.md): 난독화·백업·무결성
- [패키지](references/packages.md)
- [암호·생체 인증](references/crypto.md)
