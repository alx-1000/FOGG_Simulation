
def log_game(game):
    print("--- Phase 1 ---")

    for i, action in enumerate(game.history, start=1):

        if action["type"] == "put":
            print(
                f'{i}:',
                f'Player:{action["player"]}',
                'put',
                f'({action["x"]}, {action["y"]})',
                f'{action["piece"].color1}{action["piece"].color2}',
                f'{action["direction1"]}{action["direction2"]}'
            )
        elif action["type"] == "pass":
            print(
                f'{i}:',
                f'Player:{action["player"]}',
                'pass'
            )
        elif action["type"] == "end_phase":
            print(
                f'{i}:',
                f'Player:{action["player"]}',
                'end phase',
                f'{action["phase"] - 1}',
                'score:',
                f'F:{action["score_F"]}',
                f'G:{action["score_G"]}'
            )
            print()
            print(f"--- Phase {action['phase']} ---")

        elif action["type"] == "game_end":
            print()
            print(
                f'Game end ({action["reason"]})',
                'final score:',
                f'F:{action["score_F"]}',
                f'G:{action["score_G"]}'
            )
            