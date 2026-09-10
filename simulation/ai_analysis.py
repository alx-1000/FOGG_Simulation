import argparse
import csv
from collections import Counter, defaultdict


def mean(values):
    return sum(values) / len(values) if values else 0.0


def player_ai(row, player):
    return row[f"{player}_ai"]


def print_matchup_results(rows):
    print("=== Matchup results ===")
    groups = defaultdict(list)
    for row in rows:
        groups[(row["F_ai"], row["G_ai"])].append(row)

    for (f_ai, g_ai), games in sorted(groups.items()):
        result = Counter(row["winner"] for row in games)
        f_margins = [int(row["score_F"]) - int(row["score_G"]) for row in games]
        print(f"{f_ai} (F) vs {g_ai} (G): N={len(games)}")
        print(
            f"  F wins {result['F'] / len(games):.1%}, "
            f"G wins {result['G'] / len(games):.1%}, "
            f"draws {result['draw'] / len(games):.1%}, "
            f"mean F-G margin {mean(f_margins):+.2f}"
        )


def print_ai_results(rows):
    print("\n=== AI results by side ===")
    results = defaultdict(Counter)
    for row in rows:
        for player in ("F", "G"):
            ai = player_ai(row, player)
            if row["winner"] == "draw":
                results[(ai, player)]["draw"] += 1
            elif row["winner"] == player:
                results[(ai, player)]["win"] += 1
            else:
                results[(ai, player)]["loss"] += 1

    for (ai, side), result in sorted(results.items()):
        total = sum(result.values())
        print(
            f"{ai} as {side}: N={total}, win {result['win'] / total:.1%}, "
            f"loss {result['loss'] / total:.1%}, draw {result['draw'] / total:.1%}"
        )


def print_phase_end_results(rows):
    print("\n=== Phase end choices ===")
    for phase in (1, 2):
        groups = defaultdict(list)
        for row in rows:
            end_player = row[f"phase{phase}_end_player"]
            end_ai = player_ai(row, end_player)
            groups[(end_player, end_ai)].append(row)

        print(f"Phase {phase}")
        for (player, ai), games in sorted(groups.items()):
            wins = sum(row["winner"] == player for row in games)
            draws = sum(row["winner"] == "draw" for row in games)
            empty_cells = [int(row[f"phase{phase}_empty_cells_at_end"]) for row in games]
            print(
                f"  {player} ({ai}) ended: N={len(games)}, "
                f"own win {wins / len(games):.1%}, draw {draws / len(games):.1%}, "
                f"mean empty cells {mean(empty_cells):.2f}"
            )


def print_decision_results(rows):
    monte_carlo_rows = [row for row in rows if row["ai"] == "monte_carlo"]
    if not monte_carlo_rows:
        return

    print("\n=== Monte Carlo decision quality ===")
    groups = defaultdict(list)
    for row in monte_carlo_rows:
        groups[(row["phase"], row["action_kind"])].append(row)

    for (phase, action_kind), decisions in sorted(groups.items()):
        selected_rates = [float(row["selected_win_rate"]) for row in decisions]
        gaps = [float(row["best_win_rate_gap"]) for row in decisions if row["best_win_rate_gap"] != ""]
        legal = [int(row["legal_actions"]) for row in decisions]
        evaluated = [int(row["evaluated_candidates"]) for row in decisions]
        print(
            f"Phase {phase}, {action_kind}: N={len(decisions)}, "
            f"selected win rate {mean(selected_rates):.3f}, "
            f"best-second gap {mean(gaps):.3f}, "
            f"legal actions {mean(legal):.1f}, evaluated {mean(evaluated):.1f}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", default="simulation/ai_games.csv")
    parser.add_argument("--decisions", default="simulation/ai_games_decisions.csv")
    args = parser.parse_args()

    with open(args.games, newline="", encoding="utf-8") as file:
        games = list(csv.DictReader(file))
    with open(args.decisions, newline="", encoding="utf-8") as file:
        decisions = list(csv.DictReader(file))

    print_matchup_results(games)
    print_ai_results(games)
    print_phase_end_results(games)
    print_decision_results(decisions)


if __name__ == "__main__":
    main()
