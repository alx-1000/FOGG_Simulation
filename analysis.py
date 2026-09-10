import csv
from collections import defaultdict

# CSV読み込み
with open("random_games_compare.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))


# ==========================================
# ② Phase 1 得点比較
# ==========================================

print("=== Phase 1 得点比較 ===")

for rule in ["by_player", "fixed"]:
    data = [r for r in rows if r["rule"] == rule]

    f_scores = [int(r["score_F_phase1"]) for r in data]
    g_scores = [int(r["score_G_phase1"]) for r in data]

    f_avg = sum(f_scores) / len(f_scores)
    g_avg = sum(g_scores) / len(g_scores)
    diff_avg = f_avg - g_avg

    f_lead = sum(f > g for f, g in zip(f_scores, g_scores))
    g_lead = sum(g > f for f, g in zip(f_scores, g_scores))
    draw = sum(f == g for f, g in zip(f_scores, g_scores))

    print(f"\n--- {rule} ---")
    print(f"F平均: {f_avg:.3f}")
    print(f"G平均: {g_avg:.3f}")
    print(f"平均得点差 (F-G): {diff_avg:.3f}")
    print(f"Fリード: {f_lead} ({f_lead/len(data)*100:.1f}%)")
    print(f"Gリード: {g_lead} ({g_lead/len(data)*100:.1f}%)")
    print(f"同点: {draw} ({draw/len(data)*100:.1f}%)")


# ==========================================
# ③ Phase 2 得点比較
# ==========================================

print("\n\n=== Phase 2 得点比較 ===")

for rule in ["by_player", "fixed"]:
    data = [r for r in rows if r["rule"] == rule]

    f_scores = [int(r["score_F_phase2"]) for r in data]
    g_scores = [int(r["score_G_phase2"]) for r in data]

    f_avg = sum(f_scores) / len(f_scores)
    g_avg = sum(g_scores) / len(g_scores)
    diff_avg = f_avg - g_avg

    print(f"\n--- {rule} ---")
    print(f"F平均: {f_avg:.3f}")
    print(f"G平均: {g_avg:.3f}")
    print(f"平均得点差 (F-G): {diff_avg:.3f}")


# ==========================================
# ④ 最終スコア差
# ==========================================

print("\n\n=== 最終スコア差 ===")

for rule in ["by_player", "fixed"]:
    data = [r for r in rows if r["rule"] == rule]

    diffs = [
        int(r["score_F"]) - int(r["score_G"])
        for r in data
    ]

    avg = sum(diffs) / len(diffs)
    max_diff = max(diffs)
    min_diff = min(diffs)

    f_ahead = sum(d > 0 for d in diffs)
    g_ahead = sum(d < 0 for d in diffs)
    draw = sum(d == 0 for d in diffs)

    print(f"\n--- {rule} ---")
    print(f"平均スコア差 (F-G): {avg:.3f}")
    print(f"最大差: {max_diff}")
    print(f"最小差: {min_diff}")
    print(f"Fリード: {f_ahead} ({f_ahead/len(data)*100:.1f}%)")
    print(f"Gリード: {g_ahead} ({g_ahead/len(data)*100:.1f}%)")
    print(f"同点: {draw} ({draw/len(data)*100:.1f}%)")


# ==========================================
# ⑤ Phase 1の得点差 → 最終勝敗
# ==========================================

print("\n\n=== Phase 1得点差と最終勝敗 ===")

for rule in ["by_player", "fixed"]:

    print(f"\n--- {rule} ---")

    groups = defaultdict(list)

    data = [r for r in rows if r["rule"] == rule]

    for r in data:
        phase1_diff = (
            int(r["score_F_phase1"])
            - int(r["score_G_phase1"])
        )

        groups[phase1_diff].append(r)

    for diff in sorted(groups):

        group = groups[diff]
        n = len(group)

        f = sum(r["winner"] == "F" for r in group)
        g = sum(r["winner"] == "G" for r in group)
        draw = sum(r["winner"] == "draw" for r in group)

        print(
            f"Phase1差 {diff:+}: "
            f"N={n}, "
            f"F={f/n*100:.1f}%, "
            f"G={g/n*100:.1f}%, "
            f"draw={draw/n*100:.1f}%"
        )
print("\n\n=== Phase 1 → 最終勝敗：逆転率 ===")

for rule in ["by_player", "fixed"]:

    data = [r for r in rows if r["rule"] == rule]

    # Phase 1でF/Gがリードしていたゲーム
    f_lead_games = []
    g_lead_games = []

    for r in data:
        diff = (
            int(r["score_F_phase1"])
            - int(r["score_G_phase1"])
        )

        if diff > 0:
            f_lead_games.append(r)

        elif diff < 0:
            g_lead_games.append(r)

    # FがPhase1でリード → 最終的にGが勝った
    f_lead_reversal = sum(
        r["winner"] == "G"
        for r in f_lead_games
    )

    # GがPhase1でリード → 最終的にFが勝った
    g_lead_reversal = sum(
        r["winner"] == "F"
        for r in g_lead_games
    )

    print(f"\n--- {rule} ---")

    print(
        f"FがPhase1でリード: {len(f_lead_games)}局"
    )
    print(
        f"  → Gが逆転勝利: "
        f"{f_lead_reversal}局 "
        f"({f_lead_reversal / len(f_lead_games) * 100:.1f}%)"
    )

    print(
        f"GがPhase1でリード: {len(g_lead_games)}局"
    )
    print(
        f"  → Fが逆転勝利: "
        f"{g_lead_reversal}局 "
        f"({g_lead_reversal / len(g_lead_games) * 100:.1f}%)"
    )

print("\n\n=== Phase 1 リード幅ごとの逆転率 ===")

for rule in ["by_player", "fixed"]:

    print(f"\n--- {rule} ---")

    groups = defaultdict(list)

    data = [r for r in rows if r["rule"] == rule]

    for r in data:

        diff = (
            int(r["score_F_phase1"])
            - int(r["score_G_phase1"])
        )

        # F/Gどちらがリードしているかではなく
        # 「リードしている側から見た点差」にする
        lead = abs(diff)

        if lead > 0:
            groups[lead].append(r)

    for lead in sorted(groups):

        group = groups[lead]
        n = len(group)

        reversal = 0

        for r in group:

            phase1_diff = (
                int(r["score_F_phase1"])
                - int(r["score_G_phase1"])
            )

            # FリードなのにG勝利
            if phase1_diff > 0 and r["winner"] == "G":
                reversal += 1

            # GリードなのにF勝利
            elif phase1_diff < 0 and r["winner"] == "F":
                reversal += 1

        print(
            f"リード {lead}点: "
            f"N={n}, "
            f"逆転={reversal}局 "
            f"({reversal/n*100:.1f}%)"
        )