from play import play_random_game

for game_id in range(100):
    game = play_random_game()

    end_event = [
        event for event in game.history
        if event["type"] == "game_end"
    ][-1]

    if end_event["reason"] == "board_full":
        board = game.board[2]

        filled = sum(
            1
            for y in range(3)
            for x in range(3)
            if board[y][x] is not None
        )

        print(
            game_id + 1,
            "filled =", filled,
            "F hand =", len(game.hand["F"]),
            "G hand =", len(game.hand["G"]),
            flush=True
        )