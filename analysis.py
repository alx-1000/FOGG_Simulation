import csv
from collections import Counter


# =========================
# CSV読み込み
# =========================

with open(
    "random_games.csv",
    "r",
    encoding="utf-8"
) as f:

    rows = list(csv.DictReader(f))


# =========================
# 1. 全体の勝率
# =========================

winner_counts = Counter(
    row["winner"]
    for row in rows
)

total = len(rows)

print("=== 全体の結果 ===")
print(f"ゲーム数: {total}")
print(f"F勝利: {winner_counts['F']} ({winner_counts['F'] / total * 100:.1f}%)")
print(f"G勝利: {winner_counts['G']} ({winner_counts['G'] / total * 100:.1f}%)")
print(f"引き分け: {winner_counts['draw']} ({winner_counts['draw'] / total * 100:.1f}%)")


# =========================
# 2. Phase 1終了ターンの分布
# =========================

turn_counts = Counter(
    int(row["phase1_turns"])
    for row in rows
)

print()
print("=== Phase 1終了ターンの分布 ===")

for turns in sorted(turn_counts):
    print(
        f"{turns}ターン: "
        f"{turn_counts[turns]}ゲーム "
        f"({turn_counts[turns] / total * 100:.1f}%)"
    )


# =========================
# 3. Phase 1終了者の分布
# =========================

end_player_counts = Counter(
    row["phase1_end_player"]
    for row in rows
)

print()
print("=== Phase 1終了者 ===")

for player in ["F", "G"]:
    count = end_player_counts[player]
    print(
        f"{player}: "
        f"{count}ゲーム "
        f"({count / total * 100:.1f}%)"
    )


# =========================
# 4. Phase 1終了ターン × 終了者
# =========================

counts = Counter(
    (
        int(row["phase1_turns"]),
        row["phase1_end_player"]
    )
    for row in rows
)

print()
print("=== Phase 1終了ターン × 終了者 ===")

for turns in sorted(turn_counts):

    f = counts[(turns, "F")]
    g = counts[(turns, "G")]

    print(
        f"{turns}ターン: "
        f"F={f}, G={g}"
    )


# =========================
# 5. Phase 1終了ターン × 勝者
# =========================

print()
print("=== Phase 1終了ターン × 勝者 ===")

for turns in sorted(turn_counts):

    subset = [
        row for row in rows
        if int(row["phase1_turns"]) == turns
    ]

    n = len(subset)

    f_win = sum(row["winner"] == "F" for row in subset)
    g_win = sum(row["winner"] == "G" for row in subset)
    draw = sum(row["winner"] == "draw" for row in subset)

    print(
        f"{turns}ターン: "
        f"N={n}, "
        f"F={f_win / n * 100:.1f}%, "
        f"G={g_win / n * 100:.1f}%, "
        f"draw={draw / n * 100:.1f}%"
    )


# =========================
# 6. GがPhase 1を終了した場合
# =========================

g_end_games = [
    row for row in rows
    if row["phase1_end_player"] == "G"
]

print()
print("=== GがPhase 1を終了した場合 ===")

for turns in sorted(
    set(int(row["phase1_turns"]) for row in g_end_games)
):

    subset = [
        row for row in g_end_games
        if int(row["phase1_turns"]) == turns
    ]

    n = len(subset)

    g_win = sum(row["winner"] == "G" for row in subset)
    f_win = sum(row["winner"] == "F" for row in subset)
    draw = sum(row["winner"] == "draw" for row in subset)

    print(
        f"{turns}ターン: "
        f"N={n}, "
        f"G勝率={g_win / n * 100:.1f}%, "
        f"F勝率={f_win / n * 100:.1f}%, "
        f"draw={draw / n * 100:.1f}%"
    )


# =========================
# 7. Gの自主終了 vs 強制終了
# =========================

g_voluntary = [
    row for row in g_end_games
    if int(row["phase1_turns"]) < 9
]

g_forced = [
    row for row in g_end_games
    if int(row["phase1_turns"]) == 9
]


def print_result(name, data):

    n = len(data)

    if n == 0:
        print(f"{name}: 0ゲーム")
        return

    g_win = sum(row["winner"] == "G" for row in data)
    f_win = sum(row["winner"] == "F" for row in data)
    draw = sum(row["winner"] == "draw" for row in data)

    print()
    print(f"=== {name} ===")
    print(f"ゲーム数: {n}")
    print(f"G勝利: {g_win} ({g_win / n * 100:.1f}%)")
    print(f"F勝利: {f_win} ({f_win / n * 100:.1f}%)")
    print(f"引き分け: {draw} ({draw / n * 100:.1f}%)")


print_result(
    "Gが自主的にPhase 1終了（3〜8ターン）",
    g_voluntary
)

print_result(
    "Gが強制終了（Phase 1 = 9ターン）",
    g_forced
)