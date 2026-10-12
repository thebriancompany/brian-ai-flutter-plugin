# 공급망 보안

## 출처 확인 신호

- 유명 패키지와 한 글자·하이픈·철자 순서만 다른 이름을 확인한다.
- 검증된 배포자 여부, 저장소·홈페이지의 일치, 유지보수 기록을 확인한다.
- 파일·네트워크·카메라·키 저장소 접근 같은 권한과 실제 용도를 비교한다.
- 낮은 pub 점수나 미검증 배포자만으로 악성이라고 단정하지 않는다.

## 간접 권한 증가

앱 코드에 필요 없는 권한이 의존성 병합으로 추가되는지 확인한다.

```xml
<!-- Flag: does any first-party code actually use READ_CONTACTS? -->
<uses-permission android:name="android.permission.READ_CONTACTS" />
```

권한을 추가한 패키지를 추적한다.

```bash
flutter pub deps --style=tree
```

iOS `Info.plist`의 사용 목적 설명 키도 확인한다.

## 보안 권고

실제 설치 버전과 최신 권고를 확인한다. 인기와 안전성을 동일시하지 않는다. `dart pub get`의 권고 출력도 확인하되 별도 lockfile 검사와 구분한다.

```text
http 0.13.0 (affected by advisory: GHSA-4rgh-jx4f-xxxx, 1.2.0 available)
```

무시 항목에는 구체적인 근거를 남긴다.

```yaml
# pubspec.yaml
ignored_advisories:
  - GHSA-4rgh-jx4f-xxxx # 실제 영향받는 코드 경로를 사용하지 않음을 확인한 근거를 기록할 것
```

업데이트 가능 버전을 확인한다.

```bash
dart pub outdated
```

## OSV

해결된 `pubspec.lock`을 [OSV](https://osv.dev)와 대조한다. 설치와 실행 예제는 현재 설치 버전의 도움말을 확인해 사용한다.

```bash
# macOS
brew install osv-scanner

# Linux·CI 바이너리: https://github.com/google/osv-scanner/releases
osv-scanner --lockfile=pubspec.lock
# 출력: 취약 패키지·영향 버전·권고 링크
```
