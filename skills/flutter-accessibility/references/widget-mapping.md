# 위젯별 접근성 요구

내장 기본 동작도 테마·밀도·제약·플랫폼에 따라 달라질 수 있으므로 실제 트리를 확인한다.

| 위젯 | 확인·구현 |
| --- | --- |
| Image | 정보성 semanticLabel, 장식 excludeFromSemantics |
| Icon | 주변 레이블 또는 Semantics |
| IconButton | 목적을 알 수 있는 tooltip, 실제 조작 영역 |
| GestureDetector | 키보드·포커스·의미 동작을 추가하거나 버튼으로 대체 |
| InkWell | 사용자 정의 버튼의 label·button 역할 |
| ElevatedButton·TextButton | 설명적 문구와 실제 대상 크기 |
| TextField | 보이는 labelText·입력 목적 |
| Checkbox·Switch | ListTile 등으로 레이블·상태 연결 |
| Slider | label·value와 드래그 없는 조작 대안 |
| DropdownButton | FormField의 레이블과 펼침 상태 |
| AlertDialog | 포커스 진입·순환·닫기·복원 확인 |
| BottomSheet | 모달 여부에 맞는 포커스 관리 확인 |
| ListView | 스크롤 의미 정보와 항목 접근 |
| TabBar | 탭 상태·레이블·연결된 패널 |
| AnimatedContainer | 모션 감소 시 시간 조정 |
| Hero | 모션 감소 시 전환 생략 |
| PageRoute | 모션 감소 시 child 직접 반환 |

[Flutter 지침](https://docs.flutter.dev/ui/accessibility)과 [WCAG 해설](https://www.w3.org/WAI/WCAG22/Understanding/)을 참고한다.
