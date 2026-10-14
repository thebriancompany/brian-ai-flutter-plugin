# Brian Flutter 스킬

Flutter·Dart 개발을 위한 한국어 Codex 플러그인입니다. 개발 스킬 15개와 읽기 전용 코드 리뷰 스킬 1개, 총 68개의 스킬·참고 문서를 제공합니다.

설명, 사용 조건, 작업 절차, 참고 문서와 코드의 설명 주석을 한국어로 옮겼습니다. API·패키지명, 명령어, 예제 식별자와 테스트 데이터는 원래 의미를 유지합니다. Dart 예제 일부는 3.13 이상 문법을 사용하므로 대상 프로젝트 SDK를 먼저 확인하세요.

## 공식 지침과 적용 범위

[Effective Dart](https://dart.dev/effective-dart)와 Flutter의 [아키텍처](https://docs.flutter.dev/app-architecture/recommendations)·[성능](https://docs.flutter.dev/perf/best-practices)·[테스트](https://docs.flutter.dev/testing/overview)·[접근성](https://docs.flutter.dev/ui/accessibility) 지침을 기준으로 삼습니다. Flutter의 분야별 문서를 단일 공식 문서인 “Effective Flutter”로 인용하지 않습니다.

Bloc·Equatable·mocktail·Page/View·독립 패키지·very_good_analysis·100% 커버리지는 선택 가능한 프로젝트 관례입니다. 사용 중인 아키텍처와 도구를 먼저 따릅니다. 공식 린트 기준은 Flutter의 `flutter_lints`, Dart의 `lints`이며, 린트 통과만으로 모든 권고 준수가 보장되지는 않습니다.

공유하는 [검토 기준](skills/flutter-review/SKILL.md#공식-기준과-프로젝트-관례)과 [2026-10-14 점검 기록](docs/porting.md#2026-10-14-공식-지침-대조와-예제-수정)에 차이와 수정 내역을 정리했습니다. 새 Dart 문법은 설치 SDK뿐 아니라 `pubspec.yaml`의 SDK 하한이 정하는 **언어 버전**과 코드 생성기 지원도 확인해야 합니다.

## 설치

플러그인 설치와 개별 스킬 설치 중 **하나만** 선택하세요. 두 방식으로 함께 설치하면 동일 스킬이 중복 표시될 수 있습니다.

### Codex 플러그인

이 저장소의 루트에서 실행합니다.

```sh
codex plugin marketplace add .
codex plugin add brian-ai-flutter-plugin@brian-flutter-local
```

`plugin add`를 지원하지 않는 버전에서는 데스크톱 앱을 다시 열고 플러그인 목록에서 **Brian Flutter 스킬** 로컬 마켓플레이스를 선택해 설치하세요. 설치 후 새 채팅에서 스킬 목록을 확인합니다. 저장소 파일 생성만으로 개인 Codex에 자동 설치되지는 않습니다.

루트 `plugin.json`은 표준 패키지 선언이며 `.codex-plugin/plugin.json`도 호환용으로 제공합니다. 마켓플레이스의 `source.path`는 이 저장소 루트를 가리킵니다. 관련 형식은 [공식 플러그인 문서](https://developers.openai.com/plugins/build/plugins)를 따릅니다.

### 개별 스킬

Python 3.9 이상만 필요하며 별도 패키지는 설치하지 않습니다.

```sh
# 개인 스킬 경로에 설치할 내용 확인
python3 scripts/install_skills.py --dry-run

# ~/.agents/skills에 전체 설치
python3 scripts/install_skills.py

# 특정 프로젝트에만 설치
python3 scripts/install_skills.py --dest /path/to/flutter-app/.agents/skills

# 기존 설치본은 백업 후 갱신
python3 scripts/install_skills.py --replace
```

내용이 같은 스킬은 유지합니다. 다른 내용이 있으면 기본적으로 중단하며, `--replace`를 지정하면 대상 디렉터리 옆 `.skill-backups/`에 기존 스킬을 보관합니다. 다른 이름의 스킬은 건드리지 않습니다. 서로 참조하는 스킬이 있으므로 전체 묶음을 설치합니다. 각 스킬에 MIT 고지도 함께 설치됩니다.

Codex의 로컬 스킬 검색 경로는 [공식 스킬 문서](https://learn.chatgpt.com/docs/build-skills)에 설명되어 있습니다.

## 사용

설치한 스킬은 설명에 맞는 요청에서 자동으로 선택될 수 있습니다. 개별 설치에서는 다음처럼 명시적으로 호출할 수 있습니다. 플러그인 설치에서는 스킬 선택기에 표시된 이름을 선택하세요.

```text
$flutter-bloc 로그인 Bloc과 테스트를 작성해 줘.
$flutter-layered-architecture 날씨 앱의 API·저장소·화면 구조를 잡아 줘.
$flutter-accessibility 이 화면을 WCAG AA 기준으로 Android와 iOS에서 검토해 줘.
$flutter-green-gate 이 패키지의 분석·포맷·테스트·커버리지를 확인하고 실패를 수정해 줘.
$flutter-review 현재 변경된 Dart 코드를 읽기 전용으로 리뷰해 줘.
```

| 스킬 | 용도 |
| --- | --- |
| [flutter-accessibility](skills/flutter-accessibility/SKILL.md) | WCAG와 6개 플랫폼의 접근성 |
| [flutter-animations](skills/flutter-animations/SKILL.md) | 암시적·명시적 모션, 화면 전환 |
| [flutter-bloc](skills/flutter-bloc/SKILL.md) | Bloc·Cubit·상태·이벤트·테스트 |
| [flutter-create-project](skills/flutter-create-project/SKILL.md) | 새 프로젝트·패키지 생성 |
| [flutter-green-gate](skills/flutter-green-gate/SKILL.md) | 분석·포맷·테스트·커버리지 반복 |
| [flutter-internationalization](skills/flutter-internationalization/SKILL.md) | ARB·지역화·RTL |
| [flutter-layered-architecture](skills/flutter-layered-architecture/SKILL.md) | 데이터·저장소·비즈니스 로직·화면 |
| [flutter-license-compliance](skills/flutter-license-compliance/SKILL.md) | 직접·간접 의존성 라이선스 |
| [flutter-lint-upgrade](skills/flutter-lint-upgrade/SKILL.md) | very_good_analysis 갱신 |
| [flutter-material-theming](skills/flutter-material-theming/SKILL.md) | 색상·서체·컴포넌트·간격 |
| [flutter-navigation](skills/flutter-navigation/SKILL.md) | go_router·리다이렉트·딥 링크 |
| [flutter-review](skills/flutter-review/SKILL.md) | 변경된 Dart 코드 리뷰 |
| [flutter-sdk-upgrade](skills/flutter-sdk-upgrade/SKILL.md) | SDK·pubspec·CI 업그레이드 |
| [flutter-static-security](skills/flutter-static-security/SKILL.md) | 비밀값·저장·통신·의존성 보안 |
| [flutter-testing](skills/flutter-testing/SKILL.md) | 단위·위젯·골든 테스트 |
| [flutter-ui-package](skills/flutter-ui-package/SKILL.md) | 공유 위젯·디자인 토큰·Widgetbook |

## 도구와 실행 방식

스킬을 읽는 데 Flutter SDK나 MCP 서버는 필요하지 않습니다. 실제 생성·분석·테스트에는 해당 프로젝트의 Dart·Flutter SDK가 필요합니다. 일부 생성·라이선스·커버리지 작업은 `very_good_cli`를 사용하며, 연결된 MCP가 없으면 설치된 CLI를 사용합니다. 도구 설치와 프로젝트 변경은 실행 환경의 권한을 따릅니다.

편집 직후 자동 실행되는 전용 훅은 포함하지 않습니다. 품질 검사는 `flutter-green-gate`가 명시적으로 수행합니다. 리뷰 스킬의 읽기 전용 지시는 OS 수준의 실행 격리가 아니므로 엄격한 격리가 필요하면 Codex의 읽기 전용 권한을 함께 사용하세요.

## 검증과 배포 파일

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package_plugin.py
```

마지막 명령은 `dist/brian-ai-flutter-plugin-0.1.0.zip`을 만듭니다. 패키지에 스킬·참고 문서·MIT 고지가 포함되는지 검증한 뒤 압축합니다. Flutter 예제는 교육용 조각이므로 이 저장소 자체를 `flutter test`로 실행하는 구조는 아닙니다.

이식 범위와 의도적인 수정은 [전환 기록](docs/porting.md), 원본 파일 해시와 대상 매핑은 [이식 목록](docs/import-manifest.json)에 있습니다.

## 라이선스

[MIT](LICENSE). 설명에 브랜드 홍보 문구는 포함하지 않으며, 재배포에 필요한 원본 저작권·허가 고지는 루트와 각 스킬의 `LICENSE`에 보존합니다.
