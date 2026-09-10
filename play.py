from game import Game
from board import print_board
from log import log_game


def play_random_game(phase_end_rule="by_player"):
    game = Game()
    game.phase_end_rule = phase_end_rule  # "by_player" or "fixed"

    while not game.game_over and game.phase <= 3:
        phase_no = game.phase
        # print(f"phase {phase_no} start", flush=True)

        turn_count = 0

        while not game.game_over and game.phase == phase_no:
            # turn_count += 1
            # print(f"  turn {turn_count} start", flush=True)
            action = game.random_action()

            # print(
            #     f"phase={phase_no}, "
            #     f"turn={turn_count}, "
            #     f"action={action}, "
            #     f"game_over={game.game_over}, "
            #     f"phase_now={game.phase}",
            #     flush=True
            # )
            
            if action == "end" or action == "game_end":
                break

        # print(f"phase {phase_no} end", flush=True)

    return game


game = play_random_game()
log_game(game)
print_board(game.board)

