# 지역화 설정과 ARB

## 1. 의존성

```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: any

flutter:
  generate: true
```

## 2. l10n.yaml

프로젝트 루트에 만들고 기본 locale 순서를 의도하려면 `preferred-supported-locales`를 지정한다.

```yaml
arb-dir: lib/l10n/arb
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
nullable-getter: false
preferred-supported-locales: [en]
```

## 3. ARB 작성

`lib/l10n/arb/`에 저장한다. 예제는 영어 템플릿과 스페인어 번역이며, 실제 프로젝트 언어에 맞게 추가한다.

`app_en.arb`:

```json
{
  "@@locale": "en",
  "helloWorld": "Hello World!",
  "@helloWorld": {
    "description": "Greeting shown on the home page"
  },
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Label showing the number of items",
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  },
  "welcomeUser": "Welcome, {name}!",
  "@welcomeUser": {
    "description": "Welcome message with user name",
    "placeholders": {
      "name": {
        "type": "String"
      }
    }
  }
}
```

`app_es.arb`:

```json
{
  "@@locale": "es",
  "helloWorld": "!Hola Mundo!",
  "itemCount": "{count, plural, =0{Sin elementos} =1{1 elemento} other{{count} elementos}}",
  "welcomeUser": "!Bienvenido, {name}!"
}
```

## 4. 코드 생성

```bash
flutter gen-l10n
```

## 5. MaterialApp 연결

```dart
import 'package:flutter_localizations/flutter_localizations.dart';

const MaterialApp(
  localizationsDelegates: AppLocalizations.localizationsDelegates,
  supportedLocales: AppLocalizations.supportedLocales,
);
```

## ARB 문법

단순 문자열:

```json
{
  "helloWorld": "Hello World!",
  "@helloWorld": {
    "description": "Greeting shown on the home page"
  }
}
```

자리표시자:

```json
{
  "welcomeUser": "Welcome, {name}!",
  "@welcomeUser": {
    "description": "Welcome message with user name",
    "placeholders": {
      "name": {
        "type": "String"
      }
    }
  }
}
```

복수형:

```json
{
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Label showing the number of items",
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  }
}
```
