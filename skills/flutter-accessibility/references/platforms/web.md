# 웹 접근성

웹이 대상일 때 읽는다. NVDA·JAWS와 Chrome, VoiceOver와 Safari, TalkBack과 Chrome 등 실제 지원 조합을 확인한다. 브라우저 확대·`forced-colors`·`prefers-reduced-motion`도 검사한다.

## 검사

| 영역 | 확인 | 기준 |
| --- | --- | --- |
| 의미 정보 | DOM의 이름·역할·상태와 이미지 대체 텍스트 | 1.1.1·4.1.2 A |
| 대상 | 실제 CSS 크기와 간격·예외 | 2.5.8 AA |
| 포커스 | 툴팁·메뉴의 닫기·포인터 이동·유지 | 1.4.13 AA |
| 키보드 | HtmlElementView와 Flutter 사이 포커스 전달 | 2.1.1 A |
| 배치 | 320 CSS px 리플로와 확대 | 1.4.10 AA |
| 언어 | 페이지·언어 변경 부분의 lang | 3.1.1 A·3.1.2 AA |
| 폼 | 레이블·자동 완성·비밀번호 관리자 | 1.3.5·3.3.8 AA |
| 이동 | 설명적 페이지 제목과 반복 영역 건너뛰기 | 2.4.1·2.4.2 A |

## 검증

Chrome 접근성 트리, Lighthouse, axe와 실제 화면 낭독을 함께 사용한다. 자동 결과만으로 Flutter의 동적 동작·전체 적합성을 보장하지 않는다.

## Flutter 확인 사항

Flutter 웹의 의미 정보 활성화 방식을 [공식 문서](https://docs.flutter.dev/ui/accessibility/web-accessibility)와 대조한다. 필요하면 앱 시작 시 활성화할 수 있으며 핸들 수명을 관리한다.

```dart
void main() {
  runApp(const MyApp());
  if (kIsWeb) {
    SemanticsBinding.instance.ensureSemantics();
  }
}
```

- SemanticsRole의 실제 ARIA 매핑과 SDK 지원을 확인한다.
- TextFormField의 레이블이 DOM에 전달되는지 검사한다. 과거 버전의 회귀를 현재 버전에도 남아 있다고 단정하지 않는다.
- headingLevel과 페이지 제목의 실제 DOM 표현을 확인한다.
- 모션 감소 설정이 Flutter에 전달되는지 확인한다.
- identifier는 테스트용 속성이며 접근성 이름을 대신하지 않는다.
- scopesRoute·namesRoute 조합은 실제 읽기 순서와 페이지 전환으로 검증한다.

[ARIA 작성 지침](https://www.w3.org/WAI/ARIA/apg/)과 [Chrome 접근성 검사](https://developer.chrome.com/docs/lighthouse/accessibility/)를 참고한다.
