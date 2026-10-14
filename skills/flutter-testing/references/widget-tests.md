# 위젯 테스트 구조

Bloc을 사용하는 화면 예제:

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/home/home_page.dart';

import '../helpers/helpers.dart';

class _MockHomeCubit extends MockCubit<HomeState> implements HomeCubit {}

void main() {
  group(HomePage, () {
    late HomeCubit homeCubit;

    setUp(() {
      homeCubit = _MockHomeCubit();
      when(() => homeCubit.state).thenReturn(const HomeState());
    });

    Widget buildSubject() {
      return BlocProvider<HomeCubit>.value(
        value: homeCubit,
        child: const HomePage(),
      );
    }

    group('renders', () {
      testWidgets('displays welcome text', (tester) async {
        await tester.pumpApp(buildSubject());

        expect(find.text('Welcome'), findsOneWidget);
      });

      testWidgets('displays loading indicator when status is loading', (
        tester,
      ) async {
        when(() => homeCubit.state)
            .thenReturn(const HomeState(status: HomeStatus.loading));

        await tester.pumpApp(buildSubject());

        expect(find.byType(CircularProgressIndicator), findsOneWidget);
      });
    });

    group('navigates', () {
      testWidgets('to SettingsPage when settings icon is tapped', (
        tester,
      ) async {
        await tester.pumpApp(buildSubject());

        await tester.tap(find.byIcon(Icons.settings));
        await tester.pumpAndSettle();

        expect(find.byType(SettingsPage), findsOneWidget);
      });
    });

    group('calls', () {
      testWidgets('loadData when refresh button is tapped', (tester) async {
        when(() => homeCubit.loadData()).thenAnswer((_) async {});

        await tester.pumpApp(buildSubject());

        await tester.tap(find.byIcon(Icons.refresh));
        await tester.pump();

        verify(() => homeCubit.loadData()).called(1);
      });
    });
  });
}
```

## 테마와 지역화

필요한 환경을 `pumpApp`에 주입한다.

```dart
extension PumpApp on WidgetTester {
  Future<void> pumpApp(Widget widget, {ThemeData? theme}) {
    return pumpWidget(
      MaterialApp(
        theme: theme,
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: widget,
      ),
    );
  }
}
```

## 프레임 진행

| 메서드 | 용도 |
| --- | --- |
| `pumpWidget(widget)` | 최초 위젯 트리 생성 |
| `pump()` | 단일 프레임 |
| `pump(Duration)` | 지정 시간 진행 |
| `pumpAndSettle()` | 예약 프레임이 없을 때까지, 유한한 동작에만 사용 |

## 탐색

| 탐색기 | 용도 |
| --- | --- |
| `find.byType(T)` | 타입으로 찾기, 기본 선택 |
| `find.text('x')` | 사용자 문구 |
| `find.byKey(Key)` | 타입·내용이 모호할 때 |
| `find.byWidget(w)` | 특정 인스턴스 |
| `find.descendant(of, matching)` | 하위 트리 범위 제한 |

## 상호작용

```dart
// 탭
await tester.tap(find.byType(ElevatedButton));
await tester.pump();

// 텍스트 입력
await tester.enterText(find.byType(TextField), 'hello@example.com');
await tester.pump();

// 드래그·스크롤
await tester.drag(find.byType(ListView), const Offset(0, -300));
await tester.pump();

// 길게 누르기
await tester.longPress(find.byType(ListTile));
await tester.pump();
```

상호작용 뒤에는 `pump()` 등으로 프레임을 진행해야 새 상태를 검증할 수 있다.
