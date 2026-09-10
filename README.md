# Board Game Simulation

3×3×3の立体ボードにL字型の駒を配置し、ライン上の色の組み合わせによって得点を競う2人用ボードゲーム。

ゲームルールはPythonで実装済み。現在は、**大量シミュレーションによるゲーム性の分析と、戦略AIの開発**を進めている。

---

## Current Status

* ゲームルール：実装済み
* 合法手生成：実装済み
* Phase 1〜3：実装済み
* ぶら下げ配置：実装済み
* 得点計算：実装済み
* ランダムプレイによる1000局シミュレーション：実施済み
* Phase終了ルールの比較：実施済み
* Monte Carlo AI：初期実装・検証済み
* 今後：Monte Carlo AIの精度検証、MCTS、戦略分析

ゲームルールの詳細は [`SPEC.md`](SPEC.md) を参照。

---

## Game Overview

### Players

2人対戦。

* `F`：先手
* `G`：後手

### Board

3×3×3の立体ボード。

内部表現：

```text
board[z][y][x]
```

座標軸：

```text
X / Y / Z
```

### Pieces

駒は2色の面を持つL字型の立体。

各駒は以下の情報を持つ。

```text
owner
color1
color2
direction1
direction2
```

色：

```text
R = Red
B = Blue
T = Transparent
D = Black
```

所有者と色は別の概念として扱う。

### Phases

ゲームは3つのPhaseから構成される。

```text
Phase 1 → Phase 2 → Phase 3
```

Phaseの進行・終了条件は [`SPEC.md`](SPEC.md) と現在のゲーム実装を正とする。

### Hanging Placement

Phase 2以降では、ボード端部から駒をぶら下げる配置が可能。

対象となる向き：

```text
ZX
ZY
XZ
YZ
```

ぶら下げた駒の下向きの面は下のPhaseとして扱う。

同じ面を上下両方のPhaseで二重に得点計算してはいけない。

詳細は [`SPEC.md`](SPEC.md) を参照。

---

## Important Development Rules

**既存のゲームルールを勝手に変更しないこと。**

特に以下はゲームの中核となるため、AI実装の都合で変更してはいけない。

* Phase
* ぶら下げ配置
* 駒の向き
* 合法手
* 得点計算
* 手番
* Phase終了
* ゲーム終了

仕様が不明な場合は、まず既存コードを調査する。

コードと `SPEC.md` が矛盾している場合は、どちらかを勝手に修正せず、矛盾を報告する。

AI側でゲームルールや得点計算を再実装せず、既存のゲームエンジンを利用する。

---

## AI Development

AIはゲームルールから分離する。

基本的なインターフェース：

```text
Game State
    ↓
get legal moves
    ↓
apply candidate move
    ↓
simulate / search
    ↓
evaluate result
    ↓
select move
```

現在の開発方針：

```text
Random AI
    ↓
Monte Carlo AI
    ↓
MCTS
```

AIは「人間と対戦するための強いAI」だけを目的とせず、**ゲームの戦略構造を分析するための実験装置**として利用する。

---

## Analysis Goals

特に以下を分析する。

* F/Gの勝率
* 先手・後手の有利不利
* Phaseごとの得点差
* Phase終了者と勝敗の関係
* Phase終了のタイミング
* Phase 1の得点差と最終勝敗
* 逆転率
* 各局面の合法手数
* 各手の勝率
* AIが選択した手の特徴

最終的には、

> **どのような盤面・手・Phase終了タイミングが勝敗に影響するのか**

を明らかにすることを目標とする。

---

## Repository Structure

実際のファイル構成は既存プロジェクトを優先する。

概念的には以下のように分離する。

```text
game/
    game.py
    board.py
    piece.py
    ...

ai/
    random_ai.py
    monte_carlo.py
    mcts.py

simulation/
    simulate.py

analysis/
    analysis.py

tests/

SPEC.md
README.md
```

ゲーム本体、AI、シミュレーション、分析を可能な限り分離する。

---

## Experiments

現在までの実験結果・考察は [`EXPERIMENTS.md`](EXPERIMENTS.md) にまとめる。

ルールの詳細は `SPEC.md`、実験結果は `EXPERIMENTS.md`、開発上の基本方針はこのREADMEを参照する。
