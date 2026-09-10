# Experiments

## 1. Random Play

1000 games of Random vs Random.

| Metric                         | Result |
| ------------------------------ | -----: |
| F wins                         |  53.8% |
| G wins                         |  34.9% |
| Draws                          |  11.3% |
| Average score difference (F-G) |  +0.92 |
| Average turns                  |  18.45 |

Phase 1–3の平均得点差はそれぞれ +0.269, +0.494, +0.669。

**Observation:** Random PlayでもFの優位が見られ、先手有利の傾向がある。

---

## 2. Phase Ending

Phase 1の終了者と最終勝敗を比較。

| Phase 1 ender | F win | G win | Draw |
| ------------- | ----: | ----: | ---: |
| F             | 51.0% | 39.7% | 9.3% |
| G             | 58.5% | 33.1% | 8.5% |

また、Phase終了方法を比較すると：

| Rule      | F win | G win | Draw | Avg. score diff. |
| --------- | ----: | ----: | ---: | ---------------: |
| by_player | 54.1% | 38.3% | 7.6% |           +0.886 |
| fixed     | 46.9% | 44.0% | 9.1% |           +0.121 |

**Observation:** Phase終了のタイミングは先手・後手の有利不利に大きく影響する可能性がある。

---

## 3. Phase 1 Score and Final Result

Phase 1の得点差が大きいほど、最終的な勝率も高くなる。

`by_player` の例：

| F-G | F win | G win |
| --: | ----: | ----: |
|  -2 | 11.6% | 86.0% |
|  -1 | 24.3% | 67.2% |
|   0 | 45.3% | 43.2% |
|  +1 | 70.4% | 20.0% |
|  +2 | 86.6% |  7.5% |

1点差では約70%、2点差では約87%がリード側の勝利。

一方、リードの逆転率は概ね低く、1点差では約20%、2点差では約10%程度。

**Observation:** Phase 1の結果は最終勝敗の強い予測因子になっている。

---

## 4. Monte Carlo AI

Monte Carlo AI vs Random AI、30 games、10 rollouts、candidate limit 24。

| Match              | AI wins | Losses | Draws |
| ------------------ | ------: | -----: | ----: |
| MC(F) vs Random(G) |      30 |      0 |     0 |
| Random(F) vs MC(G) |      30 |      0 |     0 |

**Observation:** 少ないrollout数でもRandom AIに対して非常に強い結果が得られた。先手・後手の両方で勝っているため、単純な先手有利だけでは説明できない。

ただし、30 games / 10 rolloutsでは十分な評価とはいえない。

---

## 5. Next Experiments

* Monte Carloのrollout数を変える
* candidate limitを変える
* Phase終了をAIの候補から除外して比較する
* AIがどのようなPhase終了タイミングを選ぶか分析する
* その後MCTSを導入する
