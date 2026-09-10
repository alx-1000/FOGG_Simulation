import csv
from play import play_random_game

results = []

for phase_end_rule in ["by_player", "fixed"]:

    print(f"=== {phase_end_rule} ===")

    for game_id in range(1000):

        game = play_random_game(phase_end_rule)

        phase1_turns = 0
        phase2_turns = 0
        phase1 = None
        phase2 = None
        current_phase = 1

        for event in game.history:

            if event["type"] == "put":

                if current_phase == 1:
                    phase1_turns += 1

                elif current_phase == 2:
                    phase2_turns += 1

            elif event["type"] == "end_phase":

                if event["phase"] == 2:
                    phase1 = event
                    current_phase = 2

                elif event["phase"] == 3:
                    phase2 = event
                    current_phase = 3

        # 異常チェック
        if phase1 is None or phase2 is None:
            print("ERROR")
            print("rule:", phase_end_rule)
            print("game_id:", game_id + 1)
            print("phase1:", phase1)
            print("phase2:", phase2)

            for event in game.history:
                print(event)

            break

        # 勝者
        if game.score_F > game.score_G:
            winner = "F"

        elif game.score_G > game.score_F:
            winner = "G"

        else:
            winner = "draw"

        results.append({
            "rule": phase_end_rule,
            "game_id": game_id + 1,

            "score_F_phase1": phase1["score_F"],
            "score_G_phase1": phase1["score_G"],

            "score_F_phase2": phase2["score_F"],
            "score_G_phase2": phase2["score_G"],

            "score_F": game.score_F,
            "score_G": game.score_G,

            "winner": winner,

            "phase1_turns": phase1_turns,
            "phase1_end_player": phase1["player"],

            "phase2_turns": phase2_turns,
            "phase2_end_player": phase2["player"],
        })

        if (game_id + 1) % 100 == 0:
            print(f"{game_id + 1} games finished")


# CSV保存
with open(
    "random_games_compare.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    fieldnames = results[0].keys()

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)

print("CSV saved.")