# Game Specification

この文書はゲームルールの仕様書である。

## 1. 基本構造

### 1.1 プレイヤー

2人対戦。

```text
F
G
```

先手はF。

### 1.2 ボード

3×3×3の立体ボード。

座標：

```text
X: x
Y: y
Z: z
```

内部表現：

```python
board[z][y][x]
```

各座標は0〜2の3値を取る。

---

# 2. 駒

## 2.1 駒の構造

1つの駒は2色の面を持つL字型の立体。

概念的には、

```text
Piece(
    owner,
    color1,
    color2,
    direction1,
    direction2
)
```

で表現される。

## 2.2 所有者

所有者：

```text
F
G
```

所有者と色は独立。

## 2.3 色

```text
R = Red
B = Blue
T = Transparent
D = Black
```

## 2.4 面の向き

各面にはX/Y/Z方向の向きが設定される。

L字型の2面について、それぞれの方向を保持する。

正面・裏面という概念ではなく、立体上の2つの面の方向として扱う。

---

# 3. Phase

ゲームには3つのPhaseが存在する。

```text
Phase 1
Phase 2
Phase 3
```

基本的にはPhase nではn番目の層を対象とする。

Phase 1：

```text
第1層
```

Phase 2：

```text
第2層
```

Phase 3：

```text
第3層
```

Phaseの内部的な座標表現は現在のコードを正とする。

---

# 4. 通常配置

各Phaseで、そのPhaseに対応する層への駒の配置を行う。

合法配置条件は現在のゲーム実装を正とする。

AIが合法手を生成する場合は、既存の合法手生成処理を利用する。

AI側で合法配置条件を再実装しない。

---

# 5. ぶら下げ配置

## 5.1 対象

Phase 2以降では、ボードの端から駒をぶら下げる配置が可能。

## 5.2 向き

現在の実装で使用される代表的な向き：

```text
ZX
ZY
XZ
YZ
```

XまたはY方向が下向きになる。

## 5.3 Phaseとの関係

ぶら下げられた駒の下向きの面は、下のPhaseに属するものとして扱う。

例えば、Phase 2の駒から下向きに伸びる面は、Phase 1側の面として扱う。

### 重要なルール

下向きの面を、

```text
下のPhase
```

として計算する。

同じ面を、

```text
上のPhase
```

としても計算してはいけない。

つまり、Phase境界をまたぐ駒については面を二重計上しない。

また、ぶら下げ対象の下側が空いているか占有されているかは、ぶら下げ配置の判定において単純な禁止条件にはならない。

---

# 6. Phase終了

各プレイヤーはPhaseを終了させる行動を持つ。

Phase終了は通常の駒配置とは区別する。

ログでは必ず、

```text
phase
phase_end_player
turn
```

などを区別して記録する。

## 6.1 強制Phase移行

現在の層が埋まり、通常の配置ができなくなった場合など、ルール上必要な場合にはPhase移行が強制される。

この処理は既存実装を正とする。

「プレイヤーが自発的にPhaseを終了した場合」と「ルールによってPhaseが終了・移行した場合」は、分析上可能なら区別する。

---

# 7. 得点

得点はボード上のラインについて判定する。

対象となる方向：

```text
X
Y
Z
```

ライン上の状態から論理的な条件を評価し、得点を計算する。

詳細な得点条件は既存コードを正とする。

### 実装上の原則

得点計算をAI側で複製しない。

例えば、

```python
score = game.calculate_score(state)
```

のように、ゲームエンジンが提供する得点計算を利用する。

---

# 8. ゲーム状態

AIおよびシミュレーションでは、少なくとも以下の状態を取得できることが望ましい。

```text
board
current_player
phase
turn
scores
game_over
```

さらに分析のため、

```text
phase_end_player
phase_end_turn
legal_moves
```

なども取得できるようにする。

---

# 9. 合法手

AIが利用する合法手は、ゲームルールを満たす全ての手。

合法手には通常の駒配置だけでなく、ルール上可能なPhase終了なども含める。

理想的には、

```python
moves = get_legal_moves(state)
```

によって現在局面の全合法手を取得できるようにする。

各手は、

```python
new_state = apply_move(state, move)
```

によって状態を遷移させられるものとする。

---

# 10. ゲーム状態と状態遷移

AI実装のため、ゲームを以下のように扱えることを目標とする。

```text
State
  │
  ├── get_legal_moves()
  │
  ▼
Move
  │
  ├── apply_move()
  │
  ▼
New State
```

重要：

AIはゲームルールを持つのではなく、ゲームエンジンに問い合わせる。

---

# 11. AI

## 11.1 Random AI

最初の基準AI。

現在の合法手からランダムに1つ選択する。

```python
move = random.choice(get_legal_moves(state))
```

Random AI同士を大量対戦し、ゲームそのものに先手有利などの基本的な偏りがあるか確認する。

---

## 11.2 Monte Carlo AI

各候補手について、その手を実行した後にランダムプレイアウトを大量に行う。

概念：

```text
現在局面
  │
  ├─ Move A
  │    └─ random simulation × N
  │
  ├─ Move B
  │    └─ random simulation × N
  │
  └─ Move C
       └─ random simulation × N
```

各手について、

```text
勝率
平均得点
平均得点差
```

などを計算し、最も評価の高い手を選択する。

---

# 12. MCTS

将来的にはMonte Carlo Tree Searchを実装する。

基本的には、

```text
Selection
Expansion
Simulation
Backpropagation
```

の4段階を用いる。

ただし、まずRandom AIとMonte Carlo AIを実装してゲームの分析基盤を確立する。

---

# 13. AIの評価

AIの評価は単純な勝率だけでは行わない。

各候補手について可能なら、

```text
win rate
average final score
average score difference
Phase 1 end probability
Phase 2 end probability
opponent win rate
```

などを記録する。

---

# 14. 重要なゲーム性分析

本ゲームでは、Phase終了のタイミングが重要な戦略要素と考えられる。

そのため、特に以下を分析する。

### Phase 1

```text
Fが終了
Gが終了
同一条件
```

と最終勝率の関係。

### Phase 2

同様に、

```text
Fが終了
Gが終了
```

と最終勝率の関係。

### 手との関係

ある手を選択した結果、

```text
Phase終了者
Phase終了タイミング
最終勝率
```

がどのように変化するかを見る。

---

# 15. シミュレーションログ

1ゲーム1行のCSVだけでなく、必要に応じて「1手1行」のログも作成する。

## Game-level log

例：

```text
game_id
winner
final_score_F
final_score_G
phase1_end_player
phase2_end_player
phase3_end_player
total_turns
```

## Turn-level log

例：

```text
game_id
turn
player
phase
move
score_F
score_G
num_legal_moves
phase_end
```

AI分析ではTurn-level logを特に重視する。

---

# 16. 再現性

ランダムシミュレーションではrandom seedを設定可能にする。

例：

```python
simulate(seed=12345)
```

同じseedを与えた場合、可能な限り同じ結果を再現できるようにする。

---

# 17. テスト

AIを実装する前に、ゲームエンジンのテストを作る。

特にテストすべき項目：

* 3×3×3ボードの座標
* 駒の向き
* 通常配置
* ぶら下げ配置
* Phase移行
* 強制Phase移行
* Phase終了
* 得点計算
* ゲーム終了
* 合法手生成
* 手番切り替え

既存コードがすでにこれらを正しく実装している場合、その挙動をテストで固定する。

---

# 18. 変更方針

ゲームルールを変更する場合と、AI・分析機能を追加する場合を明確に分離する。

原則：

```text
ゲームルール
    ↓
Game Engine
    ↓
AI
    ↓
Simulation
    ↓
Analysis
```

AI実装のためにゲームルールを変更しない。

ゲームルールに問題がある可能性が見つかった場合は、AIコードを修正するのではなく、まずルールと既存実装の整合性を確認する。

---

# 19. 未確定・要確認事項

以下については、この仕様書だけから推測して実装してはいけない。

* 詳細な得点計算式
* 各駒の具体的な初期構成
* Phase終了の正確な条件
* 強制Phase移行の詳細条件
* 全ての合法配置条件
* ゲーム終了の最終条件
* 同点時の勝敗判定
* ぶら下げ配置の全ての幾何学的条件

これらは現在のPython実装を調査して確定する。

**コードとこの仕様書が矛盾する場合、勝手にどちらかを変更せず、矛盾を報告すること。**

---

# 20. 開発の優先順位

以下の順番で実装する。

### Step 1

既存ゲームを変更せず、現在のテストを作る。

### Step 2

ゲーム状態をコピーして仮想的に手を実行できるようにする。

### Step 3

合法手を統一的に取得できるAPIを作る。

```python
get_legal_moves(state)
```

### Step 4

Random AIを実装。

### Step 5

大量対戦とCSVログ生成。

### Step 6

Monte Carlo AIを実装。

### Step 7

AIの手ごとの勝率・得点・Phase終了への影響を分析。

### Step 8

必要ならMCTSを実装。

---

# 最重要原則

このプロジェクトのAIは「人間と対戦するためのAI」を第一目的としない。

**ゲームの戦略構造を分析するための実験装置としてAIを利用する。**

したがって、

```text
強いAIを作る
```

ことだけでなく、

```text
なぜその手が強いのか
どのPhaseで強いのか
Phase終了のタイミングが勝敗にどう影響するのか
どの盤面状態が有利なのか
```

を分析可能にすることを重視する。
