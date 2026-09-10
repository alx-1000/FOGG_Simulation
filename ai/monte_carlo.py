import random

from ai.random_ai import RandomAI
from ai.runner import outcome_for


class MonteCarloAI:
    """Select the move with the largest estimated win rate after random rollouts."""

    def __init__(self, rollouts_per_action=100, seed=None, candidate_limit=None):
        if rollouts_per_action < 1:
            raise ValueError("rollouts_per_action must be at least 1")
        if candidate_limit is not None and candidate_limit < 1:
            raise ValueError("candidate_limit must be at least 1")
        self.rollouts_per_action = rollouts_per_action
        self.candidate_limit = candidate_limit
        self.random = random.Random(seed)
        self.last_estimates = []

    def choose_action(self, game):
        player = game.current_player
        estimates = []
        for action in self._candidate_actions(game):
            total_outcome = 0.0
            total_margin = 0
            for _ in range(self.rollouts_per_action):
                rollout = game.clone()
                rollout.apply_action(action)
                self._play_randomly_to_end(rollout)
                total_outcome += outcome_for(rollout, player)
                own_score = rollout.score_F if player == "F" else rollout.score_G
                other_score = rollout.score_G if player == "F" else rollout.score_F
                total_margin += own_score - other_score
            estimates.append({
                "action": action,
                "win_rate": total_outcome / self.rollouts_per_action,
                "mean_score_margin": total_margin / self.rollouts_per_action,
            })

        self.last_estimates = estimates
        best_rate = max(item["win_rate"] for item in estimates)
        finalists = [item for item in estimates if item["win_rate"] == best_rate]
        best_margin = max(item["mean_score_margin"] for item in finalists)
        finalists = [item for item in finalists if item["mean_score_margin"] == best_margin]
        return self.random.choice(finalists)["action"]

    def _candidate_actions(self, game):
        actions = game.get_legal_actions()
        if self.candidate_limit is None or len(actions) <= self.candidate_limit:
            return actions

        phase_end_actions = [action for action in actions if action.kind == "end_phase"]
        other_actions = [action for action in actions if action.kind != "end_phase"]
        limit = max(0, self.candidate_limit - len(phase_end_actions))
        return phase_end_actions + self.random.sample(other_actions, limit)

    def _play_randomly_to_end(self, game):
        rollout_agent = RandomAI(self.random.randrange(2**63))
        while not game.game_over:
            game.advance_forced_actions()
            if not game.game_over:
                game.apply_action(rollout_agent.choose_action(game))
