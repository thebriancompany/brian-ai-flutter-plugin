# 한국어·Codex 전환 기록

기준 리비전은 `496a3c6d857476b3f75bc7bca292eff9ba18c7d1`, 원본 패키지 버전은 `0.0.5`입니다. 2026-10-12에 개발 스킬 15개와 그 참고 문서 67개, 리뷰어 1개를 반영했습니다. 최종 결과는 스킬 16개와 Markdown 문서 68개입니다. [파일별 매핑과 SHA-256](import-manifest.json)으로 누락을 확인할 수 있습니다.

## 번역 범위

스킬 설명·본문·표·플랫폼별 참고 문서·코드 설명 주석·보고서 양식을 한국어로 옮기고 중복 설명을 정리했습니다. API 이름·실행 명령·예제 식별자·문자열 데이터·도구의 출력 예시는 필요에 따라 유지합니다. 예제의 숫자·버전은 최신 버전으로 간주하지 않고 대상 환경에서 확인하도록 안내합니다.

브랜드 소개와 홍보 링크를 제거했습니다. 실제 의존성인 `very_good_cli`, `very_good_analysis` 등은 코드와 명령이 작동하도록 이름을 유지합니다. MIT 고지 원문은 번역하거나 삭제하지 않았습니다.

## 호스트 전환

| 원본 구성 | Codex 구성 |
| --- | --- |
| 호스트 전용 plugin manifest | 표준 plugin.json와 Codex 호환 선언 |
| 일반적인 짧은 스킬 이름 | 충돌을 줄이는 flutter- 접두사 |
| 전용 도구 허용 목록·인수·effort 필드 | name·description 및 agents/openai.yaml |
| 고정 MCP 도구 이름 | 연결 도구의 실제 스키마 확인, CLI 대안 |
| 전용 사용자 질문 API | Codex 질문 도구 또는 일반 텍스트 |
| 편집 이벤트의 분석·포맷 훅 | flutter-green-gate의 명시적 실행과 최종 검증 |
| 자동 주입된 리뷰어 기준과 명령 차단 훅 | flutter-review의 문서 읽기·범위 제한·읽기 전용 절차 |
| 호스트 전용 평가 하네스 | 설치·패키징 테스트와 스킬 구조 검증 |

원본의 전용 훅·평가 실행기·릴리스 자동화·저장소 운영 문서는 배포물에 복사하지 않았습니다. 해당 훅이 실행되거나 명령을 차단한다고 주장하는 문구도 제거했습니다. 개인 Codex 설정이나 계정의 연결은 자동으로 변경하지 않습니다.

## 의도적인 동작 조정

- 사용자가 이미 정한 버전·도구·아키텍처·수정 범위를 존중합니다. 같은 요청을 반복해야만 허용하던 규칙과 일괄적인 추가 승인 절차를 제거했습니다.
- SDK와 린트 업그레이드에서 기존 CI 공급자를 추정하지 않습니다. 캐럿을 정확한 버전 고정이라고 부르지 않으며 Pub workspace와 독립 패키지를 구분합니다.
- 품질 검사는 같은 최종 라운드의 실제 결과를 요구합니다. 오래된 커버리지, 미실행 테스트, 0인 분모를 성공으로 처리하지 않습니다. 실패 수가 같다는 사실만으로 진전이 없다고 단정하지 않습니다.
- 라이선스 유형만으로 모든 배포가 허용된다고 판단하지 않습니다. 실제 고지·배포 조건과 검사 범위를 보고합니다.
- 접근성 문서의 과거 플랫폼 회귀는 현재 SDK에서 재현 여부를 확인하도록 바꿨습니다. 모션·목표 크기의 권장사항과 선택된 WCAG 수준의 필수 기준을 구분합니다.

## 확인하고 바로잡은 기술 설명

| 항목 | 반영 |
| --- | --- |
| pumpAndSettle | 첫 인수는 프레임 진행 간격, 제한 시간은 세 번째 인수. [Flutter API](https://api.flutter.dev/flutter/flutter_test/WidgetTester/pumpAndSettle.html) |
| Mocktail fallback | 매처의 타입 안전한 자리표시자이며 미설정 호출의 반환값이 아님. [패키지 문서](https://pub.dev/packages/mocktail) |
| go_router extra | 웹 지원 자체를 부정하지 않고 URL 복원·브라우저 직렬화 제약을 설명. [공식 패키지 문서](https://pub.dev/documentation/go_router/latest/topics/Navigation-topic.html) |
| RTL 정렬 | 존재하지 않는 AlignDirectional 대신 Align과 AlignmentDirectional 사용. [Flutter API](https://api.flutter.dev/flutter/widgets/Align-class.html) |
| WCAG 수준 | 4.1.3은 AA로 분류하고 깜박임·인증·조작 대상 크기의 예외와 조건을 정정. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| 비밀값 | 장기 서버 비밀을 앱에 내려주는 것으로 해결하지 않고 서버 처리·제한된 단기 토큰을 사용 |
| 비밀번호 | 기존 SHA-512-crypt 예제는 유지보수 참고로 한정하고 새 서버 구현은 현대적 적응형 해시를 검토. [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) |

## 검증의 범위

구조 검증은 스킬 수·원본 매핑·frontmatter·한국어 UI 메타데이터·상대 링크·코드 펜스·호스트 전용 잔여물·MIT 동봉 여부를 확인합니다. 설치 테스트는 실제 임시 디렉터리에서 실행하며 충돌 시 일부 설치 방지, 멱등성, 백업, 심볼릭 링크 거절과 복사 실패를 확인합니다.

초기 전환 시 Codex 기본 스킬 검증기에서 16개 스킬이 통과했고, 설치·배포 테스트 9개가 통과했습니다. 원본 Markdown 68개 해시를 대조했으며 Dart 예제 217개 중 215개는 설명 주석을 제외한 코드를 보존했습니다. 접근성 보고서의 수정 전후 예제 2개는 한국어 흐름과 지역화 호출에 맞게 조정했습니다.

설치된 Codex CLI에 일회성 `marketplaces` 설정을 전달한 읽기 전용 조회에서 `brian-ai-flutter-plugin@brian-flutter-local`, 버전 `0.1.0`이 `available`로 표시되는 것을 확인했습니다. 이 확인은 개인 설정을 저장하거나 플러그인을 설치·활성화하지 않습니다.

이 검증은 모든 예제를 실제 Flutter 앱에서 컴파일하거나 보조 기술·MCP 서버를 실행한 결과가 아닙니다. 예제는 앱별 타입·지역화·SDK·패키지 설정에 맞춰 통합하고 해당 프로젝트에서 분석·테스트해야 합니다.

## 2026-10-14 공식 지침 대조와 예제 수정

스킬 16개와 참고 문서 52개를 검토했습니다. 계층 분리·주입·테스트·접근성의 기본 방향은 유지하고, 공식 권고와 팀 관례의 혼동 및 예제의 구체적 오류를 수정했습니다. 위의 원본 코드 보존 수치는 초기 이식 당시의 기록이며 이번 수정 이후 코드 동일성을 의미하지 않습니다. import-manifest의 원본 해시는 출처 기록으로 보존합니다.

| 영역 | 발견과 조치 |
| --- | --- |
| 공통·리뷰 | 네 분야만 보던 리뷰에 Effective Dart와 관련 Flutter 분야의 기준을 추가. 오류·수명·불변성·import·언어 버전과 권고 강도를 구분 |
| Bloc | 모든 테스트에 blocTest·모킹·Equatable을 강제하던 규칙 완화. Cubit 구독과 Bloc Emitter 수명을 구분. 리스트 방어적 복사와 오류 초기화가 가능한 copyWith로 수정 |
| 계층 | 모든 원천을 순수 Dart 독립 패키지로 강제하지 않음. SharedPreferences 어댑터의 Flutter 의존성·초기화, HTTP 소유권·해제, 도메인 예외 변환 보완 |
| 전체 예제 | Dart 3.11 하한과 충돌하던 primary constructor를 일반 생성자로 변경. 미정의 부트스트랩 변형을 제거하고 Provider 해제 연결. Bloc 9와 함께 사용하는 bloc_test 예제를 10으로 정합화 |
| 생성 | very_good 템플릿과 공식 flutter create·dart create를 구분. Flutter 플러그인 의존 패키지를 순수 Dart로 만들지 않도록 보완 |
| 품질 검사 | 목표가 없을 때 100%를 새 통과 조건으로 부과하지 않음. 기존 CI 기준과 커버리지 측정값을 구분 |
| 테스트 | fake·mock 선택, main 수준 setup, 실제 Bloc을 사용하는 위젯 테스트의 분류 정정. 존재하지 않는 tag_overrides 제거. static 태그 클래스 대신 최상위 상수 사용. 잘못된 thenReturn 호출 수정 |
| 애니메이션 | 없는 Easing.emphasized를 지원 곡선으로 교체. 빌더에서 CurvedAnimation 리스너를 만들지 않도록 CurveTween 사용. 목록 인덱스·부모 애니메이션 변경을 반영. 모션 감소와 const 자식 재빌드 설명 보완 |
| Material·UI | static 전용 토큰·테마 클래스 예제를 최상위 선언으로 변경하고 ThemeExtension 인스턴스 패턴 유지. 테마 Data API 갱신, fromSeed를 시제품 전용으로 제한하지 않음. 재노출·파일 분리·다크 모드의 적용 범위 명시 |
| 내비게이션 | builder 4.x 공개 믹스인 및 3.x와의 차이, part 설정, 최상위 절대 경로와 중첩 URL 정합성 보완. 실제 라우터 테스트에 dispose 추가 |
| 지역화 | context.l10n은 편의 확장임을 명시. nullable-getter 설정과 확장 타입 일치, 테스트의 supportedLocales 누락 보완 |
| 접근성 | 존재하지 않는 MediaQueryData.accessibilityFeatures 제거. 확대·모션 테스트가 실제 속성을 검증하도록 수정. 키보드 활성화 검증, 아이콘 그림과 조작 영역 구분, 대비 수치 재계산, 최신 announcement API 반영 |
| 정적 보안 | 공개 Firebase 키를 서버 비밀과 구분. local_auth 3.x API와 2.x 호환 범위 명시. 로그의 사용자 식별자·원시 예외 노출 예제 정리. 별도 핀 검사와 실제 요청 보호 구분 |
| SDK·린트 업그레이드 | 기존 최소 변경·버전 확인 절차 유지. 새 문법의 언어 버전 확인과 공통 공식 기준 연결 |
| 라이선스 | 실제 해결 버전·원문·배포 조건을 확인하고 자동 법률 보증을 하지 않는 기존 범위 유지. 공통 기준 연결 |

대조한 주요 1차 자료:

- [Effective Dart](https://dart.dev/effective-dart), [Usage](https://dart.dev/effective-dart/usage), [Design](https://dart.dev/effective-dart/design), [Primary constructors](https://dart.dev/language/primary-constructors)
- [Flutter architecture recommendations](https://docs.flutter.dev/app-architecture/recommendations), [Performance best practices](https://docs.flutter.dev/perf/best-practices), [Testing overview](https://docs.flutter.dev/testing/overview)
- [MediaQueryData](https://api.flutter.dev/flutter/widgets/MediaQueryData-class.html), [Easing](https://api.flutter.dev/flutter/material/Easing-class.html), [CurvedAnimation.dispose](https://api.flutter.dev/flutter/animation/CurvedAnimation/dispose.html), [테마 정규화](https://docs.flutter.dev/release/breaking-changes/component-theme-normalization)
- [test 설정](https://github.com/dart-lang/test/blob/master/pkgs/test/doc/configuration.md), [go_router_builder 변경 기록](https://pub.dev/packages/go_router_builder/changelog), [local_auth 변경 기록](https://pub.dev/packages/local_auth/changelog), [Firebase 키](https://firebase.google.com/docs/projects/api-keys)

검증은 저장소 구조·설치·배포 검사와 별도 임시 Flutter 프로젝트의 핵심 예제 실행으로 나눕니다. Flutter 3.47.1 / Dart 3.13.1에서 접근성 예제 11개, 상태의 불변성·오류 초기화 2개, 목록 애니메이션 갱신 1개, 컴포넌트 테마 구성 1개로 총 15개 테스트와 해당 임시 프로젝트의 정적 분석이 통과했습니다. 저장소 구조 검사, 16개 스킬의 기본 검증, 설치·배포 테스트 9개와 ZIP 생성도 통과했습니다. 문서에서 해당 코드 블록을 추출하고 필요한 테스트용 모델과 import를 붙여 실행했습니다. 파싱 가능한 Dart 코드 블록 117개는 dart format으로 정리했으며 이는 타입 검사와 별개입니다.

이 결과는 전체 코드 조각의 컴파일 보증, go_router·JSON 생성기의 모든 버전 검증, 네이티브 생체 인증·화면 낭독 실행, WCAG 적합성 인증을 뜻하지 않습니다. 구문 포맷 검증과 실제 타입·동작 검증도 구분합니다. 예제 버전을 최신값으로 간주하거나 이 자료 전체가 공식 인증을 받았다고 표현하지 않습니다.
