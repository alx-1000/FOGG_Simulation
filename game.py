from piece import pieces_F, pieces_G
from board import print_board
from score import calculate_x_lines, calculate_y_lines, calculate_z_lines, calculate_score

#color
R = "R"
B = "B"
T = "T"
N = "N"

#direction
X = 'X'
Y = 'Y'
Z = 'Z'

#         x →
#      x 0 1 2
#     ┌─────────
# y 0 │
# ↓ 1 │
#   2 │

# z = 0, 1, 2

class Game:
    def __init__(self):
        self.phase = 1
        self.current_player = "F"

        self.phase_end_used = {
            "F": False,
            "G": False
        }

        self.hand = {
            "F": pieces_F.copy(),
            "G": pieces_G.copy()
        }

        self.board = [
    [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ],
    [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ],
    [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
]
    def change_turn(self):
        if self.current_player == "F":
            self.current_player = "G"
        else: 
            self.current_player = "F"

    def can_put_piece(self, x, y, piece):
        z = self.phase - 1

        # 盤面の範囲
        if x < 0 or x >= 3 or y < 0 or y >= 3:
            return False

        # そのマスが空いているか
        if self.board[z][y][x] is not None:
            return False

        # 現在のプレイヤーの駒か
        if piece not in self.hand[self.current_player]:
            return False

        return True

    def put_piece(self, x, y, piece, direction1, direction2):
        if not self.can_put_piece(x, y, piece):
            return False
        
        z = self.phase - 1  

        piece.direction1 = direction1
        piece.direction2 = direction2

        self.board[z][y][x] = piece
        self.hand[self.current_player].remove(piece)
        self.change_turn()
        return True

    def print_board(self):
        print_board(self.board)

    def calculate_score(self):
        print(f"フェーズ {self.phase} の得点計算")

    def end_phase_by_player(self):
        player = self.current_player
        if self.phase_end_used[player]:
            return False

        self.end_phase()
        self.phase_end_used[player] = True
        print(f"{player} がフェーズ {self.phase} を終了しました")

        return True

    def end_phase(self):

        self.calculate_score()

        if self.phase < 3:
            self.phase += 1

            # 次のフェーズでは再び1回終了できる
            self.phase_end_used["F"] = False
            self.phase_end_used["G"] = False

            print(f"フェーズ {self.phase} 開始")

        else:
            print(f"フェーズ {self.phase} 終了")
            print("ゲーム終了")

    def get_legal_moves(self):
        moves = []
        directions = ["X", "Y", "Z"]

        for y in range(3):
            for x in range(3):
                for piece in self.hand[self.current_player]:

                    if self.can_put_piece(x, y, piece):

                        for direction1 in directions:
                            for direction2 in directions:

                                if direction1 == direction2:
                                    continue

                                moves.append(
                                    (x, y, piece, direction1, direction2)
                                )

        return moves

    

game = Game()

moves = game.get_legal_moves()

print(len(moves))
print(moves[2])

x, y, piece, direction1, direction2 = moves[0]

result = game.put_piece(
    x, y, piece, direction1, direction2
)

print(result)




# ####デバッグ

# game = Game()


# ##phase1
# game.put_piece(0, 0, pieces_F[0], "X", "Y")
# game.put_piece(1, 0, pieces_G[0], "Z", "Y")
# game.put_piece(2, 0, pieces_F[1], "X", "Z")
# game.put_piece(0, 1, pieces_G[2], "X", "Y")
# game.put_piece(1, 1, pieces_F[4], "Z", "Y")

# print("Gがフェーズ1を終了")
# game.print_board()
# x = calculate_x_lines(game.board, game.phase)
# y = calculate_y_lines(game.board, game.phase)
# z = calculate_z_lines(game.board, game.phase)
# print('Phase1 X:', x)
# print('Phase1 Y:', y)
# print('Phase1 Z:', z)
# score_F, score_G = calculate_score(x, y, z)
# print(f"Phase1 得点 - F: {score_F}, G: {score_G}")
# game.end_phase_by_player()

# ##phase2
# game.put_piece(0, 0, pieces_G[1], "X", "Y")
# game.put_piece(1, 0, pieces_F[2], "Z", "Y")
# game.put_piece(2, 0, pieces_G[3], "X", "Z")
# game.put_piece(0, 1, pieces_F[5], "X", "Y")
# game.put_piece(1, 1, pieces_G[4], "Z", "Y")

# print("Fがフェーズ2を終了")
# game.print_board()
# x = calculate_x_lines(game.board, game.phase)
# y = calculate_y_lines(game.board, game.phase)
# z = calculate_z_lines(game.board, game.phase)
# print('Phase2 X:', x)
# print('Phase2 Y:', y)
# print('Phase2 Z:', z)
# score_F, score_G = calculate_score(x, y, z)
# print(f"Phase2 得点 - F: {score_F}, G: {score_G}")
# game.end_phase_by_player()

# ##phase3
# game.put_piece(1, 0, pieces_G[5], "Z", "Y")
# game.put_piece(2, 0, pieces_F[6], "X", "Z")
# game.put_piece(0, 1, pieces_G[6], "X", "Y")
# game.put_piece(1, 1, pieces_F[7], "Z", "Y")
# game.put_piece(2, 1, pieces_G[7], "X", "Z")
# game.put_piece(0, 2, pieces_F[8], "X", "Y")
# game.put_piece(1, 2, pieces_G[8], "Z", "Y")
# game.put_piece(2, 2, pieces_F[9], "X", "Z")
# game.put_piece(0, 0, pieces_G[9], "X", "Y")

# print("フェーズ3を終了")
# game.print_board()
# x = calculate_x_lines(game.board, game.phase)
# y = calculate_y_lines(game.board, game.phase)
# z = calculate_z_lines(game.board, game.phase)
# print('Phase3 X:', x)
# print('Phase3 Y:', y)
# print('Phase3 Z:', z)
# score_F, score_G = calculate_score(x, y, z)
# print(f"Phase3 得点 - F: {score_F}, G: {score_G}")