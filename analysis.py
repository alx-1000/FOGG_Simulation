import csv
from collections import Counter

with open("random_games_compare.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))


# =========================
# 1. 全体の結果
# =========================

print("=== 全体の結果 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]
    n = len(data)

    f_win = sum(r["winner"] == "F" for r in data)
    g_win = sum(r["winner"] == "G" for r in data)
    draw = sum(r["winner"] == "draw" for r in data)

    print()
    print(f"--- {rule} ---")
    print(f"ゲーム数: {n}")
    print(f"F勝利: {f_win} ({f_win / n * 100:.1f}%)")
    print(f"G勝利: {g_win} ({g_win / n * 100:.1f}%)")
    print(f"引き分け: {draw} ({draw / n * 100:.1f}%)")


# =========================
# 2. Phase 1終了ターン
# =========================

print()
print("=== Phase 1終了ターン ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    counts = Counter(int(r["phase1_turns"]) for r in data)

    print()
    print(f"--- {rule} ---")

    for turns in sorted(counts):
        n = counts[turns]
        print(f"{turns}手: {n}ゲーム ({n / len(data) * 100:.1f}%)")


# =========================
# 3. Phase 1終了者
# =========================

print()
print("=== Phase 1終了者 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    counts = Counter(r["phase1_end_player"] for r in data)

    print()
    print(f"--- {rule} ---")

    for player in ["F", "G"]:
        n = counts[player]
        print(f"{player}: {n}ゲーム ({n / len(data) * 100:.1f}%)")


# =========================
# 4. Phase 1終了者 × 勝者
# =========================

print()
print("=== Phase 1終了者 × 勝者 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    print()
    print(f"--- {rule} ---")

    for end_player in ["F", "G"]:

        subset = [
            r for r in data
            if r["phase1_end_player"] == end_player
        ]

        n = len(subset)

        f_win = sum(r["winner"] == "F" for r in subset)
        g_win = sum(r["winner"] == "G" for r in subset)
        draw = sum(r["winner"] == "draw" for r in subset)

        print(
            f"{end_player}が終了: "
            f"N={n}, "
            f"F={f_win / n * 100:.1f}%, "
            f"G={g_win / n * 100:.1f}%, "
            f"draw={draw / n * 100:.1f}%"
        )


# =========================
# 5. Phase 1の平均得点
# =========================

print()
print("=== Phase 1平均得点 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    f_scores = [
        int(r["score_F_phase1"])
        for r in data
    ]

    g_scores = [
        int(r["score_G_phase1"])
        for r in data
    ]

    print()
    print(f"--- {rule} ---")
    print(f"F平均: {sum(f_scores) / len(f_scores):.2f}")
    print(f"G平均: {sum(g_scores) / len(g_scores):.2f}")


# =========================
# 6. Phase 2終了時点の平均得点
# =========================

print()
print("=== Phase 2終了時点の平均得点 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    f_scores = [
        int(r["score_F_phase2"])
        for r in data
    ]

    g_scores = [
        int(r["score_G_phase2"])
        for r in data
    ]

    print()
    print(f"--- {rule} ---")
    print(f"F平均: {sum(f_scores) / len(f_scores):.2f}")
    print(f"G平均: {sum(g_scores) / len(g_scores):.2f}")


# =========================
# 7. 最終得点
# =========================

print()
print("=== 最終平均得点 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    f_scores = [int(r["score_F"]) for r in data]
    g_scores = [int(r["score_G"]) for r in data]

    print()
    print(f"--- {rule} ---")
    print(f"F平均: {sum(f_scores) / len(f_scores):.2f}")
    print(f"G平均: {sum(g_scores) / len(g_scores):.2f}")


# =========================
# 8. Phase 1得点差 × 最終勝者
# =========================

print()
print("=== Phase 1得点差 × 最終勝者 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    groups = {}

    for r in data:

        diff = (
            int(r["score_G_phase1"])
            - int(r["score_F_phase1"])
        )

        if diff not in groups:
            groups[diff] = []

        groups[diff].append(r)

    print()
    print(f"--- {rule} ---")

    for diff in sorted(groups):

        subset = groups[diff]
        n = len(subset)

        g_win = sum(r["winner"] == "G" for r in subset)
        f_win = sum(r["winner"] == "F" for r in subset)
        draw = sum(r["winner"] == "draw" for r in subset)

        print(
            f"差 {diff:+}: "
            f"N={n}, "
            f"G={g_win / n * 100:.1f}%, "
            f"F={f_win / n * 100:.1f}%, "
            f"draw={draw / n * 100:.1f}%"
        )