# 버전 해결 충돌

SDK 갱신 후 pub get이 실패하면 마지막 충돌과 그 위의 의존 경로를 함께 읽는다. 아래 출력은 설명용 예시이며 실제 패키지 제약에 대한 근거로 사용하지 않는다.

```text
Because acme_app depends on very_good_analysis >=6.0.0 <7.0.0 which requires SDK version
>=3.5.0 <3.9.0, version solving failed.
```

보고할 세 가지는 차단한 패키지·버전, 패키지가 요구하는 제약, 이번에 바꾼 제약이다.

| 형태 | 확인 | 해결 방향 |
| --- | --- | --- |
| 직접 의존성의 SDK 제한 | dependencies·dev_dependencies | 호환 버전 검토 |
| 간접 의존성의 제한 | 어떤 직접 의존성이 끌어오는지 | 상위 직접 의존성의 호환 버전 검토 |
| 호환 릴리스 없음 | 공개 버전들의 실제 제약 | SDK 목표 조정 또는 외부 수정 필요 |

간접 패키지가 pubspec에 없다고 임의의 직접 제약을 추가하지 말고 경로를 추적한다.

```bash
flutter pub deps --style=tree   # 순수 Dart는 dart pub deps --style=tree
```

## 보고 형태

```text
packages/cart_repository의 목표 SDK 의존성 해결 실패
- 차단 패키지·버전: [실제 결과]
- 해당 패키지 제약: [실제 결과]
- 목표 SDK 제약: [이번 변경]
- 의존 경로: [직접 또는 간접 경로]
- 해결 방향: [호환 버전 또는 SDK 목표 조정]
```

모노레포에서는 각 대상 결과를 모아 보고한다. 승인 범위를 벗어난 버전 완화·제거, lockfile 삭제, 무차별 `pub upgrade --major-versions`로 원인을 숨기지 않는다. 사용자가 호환 의존성 갱신을 이미 요청했다면 실제 제약을 확인해 필요한 수정과 검증을 진행한다.
