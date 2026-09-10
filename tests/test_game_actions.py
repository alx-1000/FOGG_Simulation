import unittest

from ai.monte_carlo import MonteCarloAI
from ai.random_ai import RandomAI
from ai.runner import play_game
from src.game import Action, Game


class GameActionTests(unittest.TestCase):
    def test_by_player_offers_phase_end_only_in_first_two_phases(self):
        game = Game()
        game.phase_end_rule = "by_player"
        self.assertIn(Action("end_phase"), game.get_legal_actions())
        game.phase = 3
        self.assertNotIn(Action("end_phase"), game.get_legal_actions())

    def test_fixed_does_not_offer_phase_end(self):
        game = Game()
        game.phase_end_rule = "fixed"
        self.assertNotIn(Action("end_phase"), game.get_legal_actions())

    def test_by_player_can_end_when_no_placement_is_available(self):
        game = Game()
        game.hand["F"] = []
        self.assertEqual(game.get_legal_actions(), [Action("end_phase")])

    def test_clone_does_not_change_original_game(self):
        game = Game()
        action = next(action for action in game.get_legal_actions() if action.kind == "put")
        clone = game.clone()
        clone.apply_action(action)
        self.assertEqual(game.current_player, "F")
        self.assertEqual(len(game.hand["F"]), 12)
        self.assertEqual(len(clone.hand["F"]), 11)

    def test_full_phase_three_ends_without_phase_end_action(self):
        game = Game()
        game.phase = 3
        for y in range(3):
            for x in range(3):
                game.board[2][y][x] = game.hand["F"][0]
        events = game.advance_forced_actions()
        self.assertTrue(game.game_over)
        self.assertEqual(events[-1]["reason"], "board_full")

    def test_monte_carlo_candidate_limit_keeps_phase_end_action(self):
        game = Game()
        ai = MonteCarloAI(rollouts_per_action=1, candidate_limit=3, seed=1)
        candidates = ai._candidate_actions(game)
        self.assertEqual(len(candidates), 3)
        self.assertIn(Action("end_phase"), candidates)

    def test_runner_records_decision_metrics(self):
        game = play_game({
            "F": MonteCarloAI(rollouts_per_action=1, candidate_limit=2, seed=1),
            "G": RandomAI(seed=2),
        })
        monte_carlo_decision = next(
            decision for decision in game.decision_history
            if decision["ai"] == "monte_carlo"
        )
        self.assertEqual(monte_carlo_decision["evaluated_candidates"], 2)
        self.assertNotEqual(monte_carlo_decision["selected_win_rate"], "")


if __name__ == "__main__":
    unittest.main()
