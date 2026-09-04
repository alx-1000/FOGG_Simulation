from game import Game
game = Game()

print()
print("========== GAME START ==========")
print()

while not game.game_over and game.phase <= 3:
    phase_no = game.phase
    print(f"--- Phase {phase_no} ---")

    while not game.game_over and game.phase == phase_no:
        action = game.random_action()

        if action == "end":
            print()
            print(
                f"累積得点: F={game.score_F}, "
                f"G={game.score_G}"
            )
            print()
            break

print("========== GAME END ==========")

print(f"最終得点: F={game.score_F}, G={game.score_G}")