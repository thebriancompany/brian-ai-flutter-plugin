---
name: flutter-internationalization
description: "Flutter ARB 번역, locale 설정, gen-l10n, 공유 위젯의 지역화 문자열과 RTL 배치를 추가하거나 검토할 때 사용한다."
---

# 국제화와 지역화

Flutter 기본 `flutter_localizations`·`intl`과 ARB를 사용한다. 기존 프로젝트의 지역화 도구나 사용자가 지정한 라이브러리를 요청 없이 교체하지 않는다.

## 핵심 기준

- 사용자에게 보이는 문구를 코드에 하드코딩하지 않는다.
- ARB를 번역의 기준으로 두고 `context.l10n` 확장으로 접근한다.
- 공유 위젯은 앱의 `AppLocalizations`에 직접 의존하지 않고 번역된 문자열을 매개변수로 받는다.
- 읽기 방향을 따라야 하는 여백·정렬·위치는 start/end 기반 API를 쓴다.
- 언어 하나로 시작해도 지역화 경계를 미리 고려한다.
- Dart 3.13 이상에서는 문자열 필드에 기본 생성자의 선언 매개변수를 활용하고 낮은 버전에서는 호환 문법을 유지한다.

## 구성 흐름

의존성 추가 → `pubspec.yaml`의 `generate: true` → `l10n.yaml` → `lib/l10n/arb/` → `flutter gen-l10n` → `MaterialApp`의 delegate·지원 locale 연결 순서다. ARB는 문자열·자리표시자·ICU 복수형을 지원한다.

## 컨텍스트 확장

```dart
extension AppLocalizationsX on BuildContext {
  AppLocalizations get l10n => AppLocalizations.of(this);
}
```

사용 예:

```dart
// 권장
Text(context.l10n.helloWorld);

// 피할 패턴
Text(AppLocalizations.of(context).helloWorld);
```

## 재사용 위젯

별도 패키지에 앱 지역화 클래스를 넣으면 소비 앱의 번역과 결합된다. 문자열을 `final String` 매개변수로 받고 호출부에서 `context.l10n`을 전달한다. 위젯과 호출부를 함께 보여 준다.

```dart
// 공유 위젯은 앱 지역화에 직접 의존하지 않는다.
class const ConfirmDialog({
  required final String title,
  required final String message,
  required final String confirmLabel,
  required final String cancelLabel,
  super.key,
}) extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(title),
      content: Text(message),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: Text(cancelLabel)),
        FilledButton(onPressed: () => Navigator.pop(context, true), child: Text(confirmLabel)),
      ],
    );
  }
}

// 앱 호출부에서 번역된 문자열을 전달한다.
showDialog<bool>(
  context: context,
  builder: (_) => ConfirmDialog(
    title: context.l10n.deleteTitle,
    message: context.l10n.deleteMessage,
    confirmLabel: context.l10n.confirm,
    cancelLabel: context.l10n.cancel,
  ),
);
```

## RTL

`EdgeInsetsDirectional`, `PositionedDirectional`, `AlignmentDirectional`, `BorderDirectional`을 사용한다. `Align`에는 `AlignmentDirectional`을 전달한다. 방향성이 있는 IconData는 자체 `matchTextDirection` 설정을 따르며 이미지가 반전되어야 할 때는 `Image(matchTextDirection: true)`를 사용한다.

## 백엔드

언어별 콘텐츠를 저장하고 요청·세션에서 locale을 전달한다. 오류는 상태 코드 또는 안정적인 오류 상수를 앱의 지역화 키로 매핑한다.

## 자주 하는 작업

- 언어 추가: `app_<locale>.arb`에 템플릿의 모든 키를 번역하고 생성 명령을 실행한다. 생성된 `supportedLocales`를 사용한다.
- 문구 추가: 템플릿에 키·설명·자리표시자를 추가하고 다른 언어도 갱신한다. 생성 후 `context.l10n.newKey`로 사용한다.
- 복수형: ICU 문법과 `type: int` 메타데이터를 추가하고 언어별 형식을 작성한다. `context.l10n.itemCount(items.length)`처럼 호출한다.

## 참고 문서

- [설정과 ARB](references/setup.md)
- [방향과 이미지 반전](references/directionality.md)
- [백엔드 콘텐츠와 오류](references/backend.md)
