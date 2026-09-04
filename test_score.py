from game import Game
from piece import pieces_F, pieces_G
from score import (
    calculate_x_lines,
    calculate_y_lines,
    calculate_z_lines,
    calculate_score
)


game = Game()


# ====================
# Phase 1
# ====================

game.put_piece(0, 0, pieces_F[0], "X", "Y")
game.put_piece(1, 0, pieces_G[0], "Z", "Y")
game.put_piece(2, 0, pieces_F[1], "X", "Z")
game.put_piece(0, 1, pieces_G[2], "X", "Y")
game.put_piece(1, 1, pieces_F[4], "Z", "Y")

x = calculate_x_lines(game.board, game.phase)
y = calculate_y_lines(game.board, game.phase)
z = calculate_z_lines(game.board, game.phase)

score_F, score_G = calculate_score(x, y, z)

print("Phase 1:", score_F, score_G)

game.end_phase_by_player()


# ====================
# Phase 2
# ====================

game.put_piece(0, 0, pieces_G[1], "X", "Y")
game.put_piece(1, 0, pieces_F[2], "Z", "Y")
game.put_piece(2, 0, pieces_G[3], "X", "Z")
game.put_piece(0, 1, pieces_F[5], "X", "Y")
game.put_piece(1, 1, pieces_G[4], "Z", "Y")

x = calculate_x_lines(game.board, game.phase)
y = calculate_y_lines(game.board, game.phase)
z = calculate_z_lines(game.board, game.phase)

score_F, score_G = calculate_score(x, y, z)

print("Phase 2:", score_F, score_G)

game.end_phase_by_player()


# ====================
# Phase 3
# ====================

game.put_piece(1, 0, pieces_G[5], "Z", "Y")
game.put_piece(2, 0, pieces_F[6], "X", "Z")
game.put_piece(0, 1, pieces_G[6], "X", "Y")
game.put_piece(1, 1, pieces_F[7], "Z", "Y")
game.put_piece(2, 1, pieces_G[7], "X", "Z")
game.put_piece(0, 2, pieces_F[8], "X", "Y")
game.put_piece(1, 2, pieces_G[8], "Z", "Y")
game.put_piece(2, 2, pieces_F[9], "X", "Z")
game.put_piece(0, 0, pieces_G[9], "X", "Y")

x = calculate_x_lines(game.board, game.phase)
y = calculate_y_lines(game.board, game.phase)
z = calculate_z_lines(game.board, game.phase)

score_F, score_G = calculate_score(x, y, z)

print("Phase 3:", score_F, score_G)

game.end_phase_by_player()


# ====================
# 最終確認
# ====================

assert game.phase == 3

print("1局のテストが完了しました")