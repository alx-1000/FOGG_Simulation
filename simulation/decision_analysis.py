from ai.monte_carlo import MonteCarloAI
from src.score import calculate_score, calculate_x_lines, calculate_y_lines, calculate_z_lines


def action_label(action):
    values = [action.kind]
    for name in ("x", "y", "piece_index", "direction1", "direction2", "down_direction"):
        value = getattr(action, name)
        if value is not None:
            values.append(f"{name}={value}")
    return ",".join(values)


class DecisionAnalyzer:
    """Collect Monte Carlo decision metrics without choosing moves."""

    def __init__(self, rollouts_per_action=10, seed=None, candidate_limit=24):
        if candidate_limit is not None and candidate_limit < 1:
            raise ValueError("candidate_limit must be at least 1")
        self.evaluator = MonteCarloAI(rollouts_per_action=rollouts_per_action, seed=seed)
        self.candidate_limit = candidate_limit
        self.last_detailed_rows = []
        self.detailed_rows = []

    def _analysis_actions(self, legal_actions):
        if self.candidate_limit is None or len(legal_actions) <= self.candidate_limit:
            return legal_actions

        phase_end_actions = [action for action in legal_actions if action.kind == "end_phase"]
        other_actions = [action for action in legal_actions if action.kind != "end_phase"]
        limit = max(0, self.candidate_limit - len(phase_end_actions))
        return phase_end_actions + self.evaluator.random.sample(other_actions, limit)

    def analyze(self, game, legal_actions, selected_action):
        actions = self._analysis_actions(legal_actions)
        estimates = self.evaluator.evaluate_actions(game, actions)
        self.last_detailed_rows = [
            self._describe_action(game, action, estimate, action == selected_action)
            for action, estimate in ((item["action"], item) for item in estimates)
        ]
        self.detailed_rows.extend(self.last_detailed_rows)
        ordered = sorted(estimates, key=lambda item: item["win_rate"], reverse=True)
        best = ordered[0]
        second = ordered[1] if len(ordered) > 1 else None
        worst = ordered[-1]
        selected = next(
            (item for item in estimates if item["action"] == selected_action),
            None,
        )
        best_winrate = best["win_rate"]
        second_winrate = second["win_rate"] if second else None
        worst_winrate = worst["win_rate"]
        return {
            "turn": len(getattr(game, "decision_history", [])) + 1,
            "phase": game.phase,
            "player": game.current_player,
            "legal_moves_count": len(legal_actions),
            "best_winrate": best_winrate,
            "second_winrate": second_winrate,
            "worst_winrate": worst_winrate,
            "best_second_gap": best_winrate - second_winrate if second else None,
            "best_worst_gap": best_winrate - worst_winrate,
            "selected_move": action_label(selected_action),
            "selected_winrate": selected["win_rate"] if selected else None,
        }

    def _describe_action(self, game, action, estimate, is_selected):
        before_score = (game.score_F, game.score_G)
        phase = game.phase
        before_lines = self._lines_and_score(game, phase)
        piece = None
        if action.kind == "put":
            piece = game.hand[game.current_player][action.piece_index]

        after = game.clone()
        after.apply_action(action)
        after_lines = self._lines_and_score(after, phase)
        after_score = (after.score_F, after.score_G)
        before_scored_lines = before_lines[3]
        after_scored_lines = after_lines[3]
        move_type = {
            "put": "hanging" if action.down_direction is not None else "normal",
            "end_phase": "end_phase",
            "pass": "pass",
        }[action.kind]
        return {
            "turn": len(getattr(game, "decision_history", [])) + 1,
            "phase": phase,
            "player": game.current_player,
            "move_kind": action.kind,
            "move_type": move_type,
            "x": action.x,
            "y": action.y,
            "z": phase - 1 if action.kind == "put" else None,
            "piece_index": action.piece_index,
            "owner": piece.owner if piece else None,
            "color1": piece.color1 if piece else None,
            "color2": piece.color2 if piece else None,
            "direction1": action.direction1,
            "direction2": action.direction2,
            "down_direction": action.down_direction,
            "is_hanging": action.kind == "put" and action.down_direction is not None,
            "is_end_phase": action.kind == "end_phase",
            "win_rate": estimate["win_rate"],
            "mean_score_margin": estimate["mean_score_margin"],
            "selected": is_selected,
            "immediate_score_F": after_lines[0] - before_lines[0],
            "immediate_score_G": after_lines[1] - before_lines[1],
            "immediate_score_delta": (after_lines[0] - before_lines[0]) - (after_lines[1] - before_lines[1]),
            "score_F_change": after_score[0] - before_score[0],
            "score_G_change": after_score[1] - before_score[1],
            "score_delta_change": (after_score[0] - after_score[1]) - (before_score[0] - before_score[1]),
            "completed_lines_before": before_scored_lines,
            "completed_lines_after": after_scored_lines,
            "completed_lines_change": after_scored_lines - before_scored_lines,
            "phase_end_available_before": game.can_end_phase(),
            "phase_end_available_after": after.can_end_phase(),
            "phase_full_before": game.is_phase_full(),
            "phase_full_after": after.is_phase_full(),
            "empty_cells_before": game.empty_cells_in_phase(),
            "empty_cells_after": after.empty_cells_in_phase(),
        }

    @staticmethod
    def _lines_and_score(game, phase):
        x_lines = calculate_x_lines(game.board, phase)
        y_lines = calculate_y_lines(game.board, phase)
        z_lines = calculate_z_lines(game.board, phase)
        score_F, score_G = calculate_score(x_lines, y_lines, z_lines)
        scored_lines = sum(result in ("R", "B") for result in x_lines + y_lines + z_lines)
        return score_F, score_G, x_lines + y_lines + z_lines, scored_lines