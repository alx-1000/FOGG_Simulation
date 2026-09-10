import random


class RandomAI:
    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def choose_action(self, game):
        actions = game.get_legal_actions()
        if not actions:
            raise ValueError("No selectable action in an unsettled game state")
        return self.random.choice(actions)
