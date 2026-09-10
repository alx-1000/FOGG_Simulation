from src.game import Game


def play_game(agents, phase_end_rule="by_player"):
    """Run a complete game and return the game with its complete history."""
    game = Game()
    game.phase_end_rule = phase_end_rule
    game.decision_history = []
    while not game.game_over:
        game.advance_forced_actions()
        if game.game_over:
            break
        player = game.current_player
        agent = agents[player]
        legal_actions = game.get_legal_actions()
        action = agent.choose_action(game)
        game.decision_history.append(_decision_record(game, agent, player, legal_actions, action))
        game.apply_action(action)
    return game


def outcome_for(game, player):
    opponent = "G" if player == "F" else "F"
    scores = {"F": game.score_F, "G": game.score_G}
    if scores[player] > scores[opponent]:
        return 1.0
    if scores[player] < scores[opponent]:
        return 0.0
    return 0.5


def _decision_record(game, agent, player, legal_actions, action):
    record = {
        "decision_no": len(game.decision_history) + 1,
        "player": player,
        "phase": game.phase,
        "empty_cells": game.empty_cells_in_phase(),
        "legal_actions": len(legal_actions),
        "action_kind": action.kind,
        "x": action.x,
        "y": action.y,
        "direction1": action.direction1,
        "direction2": action.direction2,
        "down_direction": action.down_direction,
        "ai": "monte_carlo" if hasattr(agent, "last_estimates") else "random",
        "evaluated_candidates": "",
        "selected_win_rate": "",
        "selected_score_margin": "",
        "best_win_rate": "",
        "second_best_win_rate": "",
        "best_win_rate_gap": "",
    }
    estimates = getattr(agent, "last_estimates", None)
    if estimates is None:
        return record

    ordered = sorted(
        estimates,
        key=lambda item: (item["win_rate"], item["mean_score_margin"]),
        reverse=True,
    )
    selected = next(item for item in estimates if item["action"] == action)
    record.update({
        "evaluated_candidates": len(estimates),
        "selected_win_rate": selected["win_rate"],
        "selected_score_margin": selected["mean_score_margin"],
        "best_win_rate": ordered[0]["win_rate"],
        "second_best_win_rate": ordered[1]["win_rate"] if len(ordered) > 1 else "",
        "best_win_rate_gap": (
            ordered[0]["win_rate"] - ordered[1]["win_rate"]
            if len(ordered) > 1 else ""
        ),
    })
    return record
