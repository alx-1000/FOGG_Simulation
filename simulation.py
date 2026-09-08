import csv

from play import play_random_game


results = []

for game_id in range(1000):

    game = play_random_game()

    # -------------------------
    # Phase情報をhistoryから取得
    # -------------------------

    phase1_turns = 0
    phase2_turns = 0

    phase1 = None
    phase2 = None

    current_phase = 1

    for event in game.history:

        # 駒を置いた
        if event["type"] == "put":

            if current_phase == 1:
                phase1_turns += 1

            elif current_phase == 2:
                phase2_turns += 1

        # Phase終了
        elif event["type"] == "end_phase":

            if event["phase"] == 2:
                # Phase 1終了
                phase1 = event
                current_phase = 2

            elif event["phase"] == 3:
                # Phase 2終了
                phase2 = event
                current_phase = 3


    # -------------------------
    # 念のためPhase情報を確認
    # -------------------------

    if phase1 is None or phase2 is None:
        print("ERROR")
        print("game_id:", game_id + 1)
        print("phase1:", phase1)
        print("phase2:", phase2)
        print("history:")
        for event in game.history:
            print(event)
        break


    # -------------------------
    # 勝者
    # -------------------------

    if game.score_F > game.score_G:
        winner = "F"

    elif game.score_G > game.score_F:
        winner = "G"

    else:
        winner = "draw"


    # -------------------------
    # CSV用データ
    # -------------------------

    results.append({

        "game_id": game_id + 1,

        # Phase 1終了時
        "score_F_phase1": phase1["score_F"],
        "score_G_phase1": phase1["score_G"],

        # Phase 2終了時
        "score_F_phase2": phase2["score_F"],
        "score_G_phase2": phase2["score_G"],

        # 最終スコア
        "score_F": game.score_F,
        "score_G": game.score_G,

        # 勝者
        "winner": winner,

        # Phase 1
        "phase1_turns": phase1_turns,
        "phase1_end_player": phase1["player"],

        # Phase 2
        "phase2_turns": phase2_turns,
        "phase2_end_player": phase2["player"],
    })


    if (game_id + 1) % 100 == 0:
        print(f"{game_id + 1} games finished")


# -------------------------
# CSV保存
# -------------------------

with open(
    "random_games.csv",
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