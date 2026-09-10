import argparse
import csv
from pathlib import Path

from ai.monte_carlo import MonteCarloAI
from ai.random_ai import RandomAI
from ai.runner import play_game


def make_agent(name, rollouts, candidate_limit, seed):
    if name == "random":
        return RandomAI(seed)
    return MonteCarloAI(rollouts, seed, candidate_limit)


def phase_end_event(game, phase):
    return next(
        event
        for event in game.history
        if event["type"] == "end_phase" and event["ended_phase"] == phase
    )


def phase_put_count(game, phase):
    return sum(
        event["type"] == "put" and event["phase"] == phase
        for event in game.history
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--rollouts", type=int, default=50)
    parser.add_argument("--candidate-limit", type=int, default=24)
    parser.add_argument("--f", choices=("random", "monte_carlo"), default="monte_carlo")
    parser.add_argument("--g", choices=("random", "monte_carlo"), default="random")
    parser.add_argument("--output", default="simulation/ai_games.csv")
    parser.add_argument("--decisions-output")
    args = parser.parse_args()

    decisions_output = args.decisions_output or str(
        Path(args.output).with_name(f"{Path(args.output).stem}_decisions.csv")
    )

    rows = []
    decision_rows = []
    for game_id in range(1, args.games + 1):
        game = play_game({
            "F": make_agent(args.f, args.rollouts, args.candidate_limit, game_id * 2),
            "G": make_agent(args.g, args.rollouts, args.candidate_limit, game_id * 2 + 1),
        })
        winner = "F" if game.score_F > game.score_G else "G" if game.score_G > game.score_F else "draw"
        phase1 = phase_end_event(game, 1)
        phase2 = phase_end_event(game, 2)
        rows.append({
            "game_id": game_id,
            "phase_end_rule": "by_player",
            "F_ai": args.f,
            "G_ai": args.g,
            "score_F_phase1": phase1["score_F"],
            "score_G_phase1": phase1["score_G"],
            "score_F_phase2": phase2["score_F"],
            "score_G_phase2": phase2["score_G"],
            "score_F": game.score_F,
            "score_G": game.score_G,
            "winner": winner,
            "turns": len(game.history),
            "phase1_turns": phase_put_count(game, 1),
            "phase1_end_player": phase1["player"],
            "phase1_end_reason": phase1["reason"],
            "phase1_empty_cells_at_end": phase1["empty_cells_at_end"],
            "phase2_turns": phase_put_count(game, 2),
            "phase2_end_player": phase2["player"],
            "phase2_end_reason": phase2["reason"],
            "phase2_empty_cells_at_end": phase2["empty_cells_at_end"],
        })
        for decision in game.decision_history:
            decision_rows.append({"game_id": game_id, **decision})

    with open(args.output, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    with open(decisions_output, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=decision_rows[0].keys())
        writer.writeheader()
        writer.writerows(decision_rows)


if __name__ == "__main__":
    main()
