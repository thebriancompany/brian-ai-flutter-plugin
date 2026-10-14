# 암호와 인증 참고

## 인증서 고정

민감한 통신에서 위협 모델에 따라 검토한다. 기본 인증서 검증을 유지하고 회전·백업 키·실패 복구를 설계한다. 아래는 패키지 API 사용 예제이며 실제 핀과 대상 호스트를 검증해야 한다.

```dart
final result = await HttpCertificatePinning.check(
  serverURL: 'https://api.example.com',
  headerHttp: {},
  sha: SHA.SHA256,
  allowedSHAFingerprints: ['AA:BB:CC:...'],
  timeout: 60,
);
if (result != 'CONNECTION_SECURE') {
  throw CertificatePinningException();
}
```

별도 check 호출 한 번만으로 이후 HTTP/Dio 요청이 고정된다고 가정하지 않는다. 실제 데이터를 전송하는 클라이언트 연결에서 검증을 강제하고 실패 시 요청을 보내지 않는다.

## 생체 인증

아래는 local_auth 3.x API다. 2.x는 AuthenticationOptions를 사용하므로 설치 버전에 맞춘다. 서버의 권한 검증을 대신하지 않으며 LocalAuthException을 처리해 실패 시 접근을 차단한다.

```dart
// 확인 필요: 플랫폼 채널로 직접 구현한 생체 인증
final result = await platform.invokeMethod('checkFingerprint');

// ✅ local_auth를 통한 생체 인증
final auth = LocalAuthentication();
final didAuthenticate = await auth.authenticate(
  localizedReason: 'Confirm your identity to view this information',
  biometricOnly: true,
);
```

## 비밀번호 해시

아래 `dart_crypt` 예제는 기존 SHA-512-crypt 구현을 읽거나 유지할 때 참고한다. 새 비밀번호 저장에는 서버에서 최신 [OWASP 지침](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)을 확인하고 Argon2id 등의 적응형 해시를 우선 검토한다. 앱에 사용자 비밀번호를 지속 저장하거나 빠른 SHA-256으로 대체하지 않는다.

```dart
import 'package:dart_crypt/dart_crypt.dart';

// 등록·비밀번호 변경 시 해시
final hashed = Crypt.sha512(password);

// 로그인 시 검증
final isValid = hashed.match(inputPassword);
```
