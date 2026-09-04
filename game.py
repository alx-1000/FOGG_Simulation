import random
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
        self.score_F = 0
        self.score_G = 0
        self.game_over = False

        self.phase_end_used = {"F": False, "G": False}
        self.hand = { "F": pieces_F.copy(),"G": pieces_G.copy()}

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

        # その駒を持っているか
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

    def end_phase_by_player(self):
        player = self.current_player
        if self.game_over or self.phase_end_used[player]:
            return False

        self.phase_end_used[player] = True
        self.end_phase()
        self.change_turn()
        return True

    def end_phase(self):
        x = calculate_x_lines(self.board, self.phase)
        y = calculate_y_lines(self.board, self.phase)
        z = calculate_z_lines(self.board, self.phase)
        score_F, score_G = calculate_score(x, y, z)
        self.score_F += score_F
        self.score_G += score_G

        if self.phase < 3:
            self.phase += 1
        else:
            self.phase = 4
            self.game_over = True

    def can_end_phase(self):
        return not self.phase_end_used[self.current_player]

    def is_phase_full(self):
        z = self.phase - 1

        for y in range(3):
            for x in range(3):
                if self.board[z][y][x] is None:
                    return False

        return True

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

    def random_move(self):
        moves = self.get_legal_moves()

        if not moves:
            return False

        move = random.choice(moves)

        x, y, piece, direction1, direction2 = move

        self.put_piece(
            x, y, piece, direction1, direction2
        )

        return True

    def random_action(self):
        if self.game_over or self.phase > 3:
            return "game_end"

        player = self.current_player

        # 段が埋まっていた場合
        if self.is_phase_full():
            if self.phase == 3:
                self.end_phase()
                return "game_end"
            
            if self.can_end_phase(): 
                self.end_phase_by_player()  
                return "end"
            else:
                self.change_turn()
                return "pass"

        moves = self.get_legal_moves()

        # 駒を持ってない?場合も
        if not moves:
            self.change_turn()
            return "pass"

        # 終了権を持っている場合
        if self.can_end_phase():

            empty_count = 0
            z = self.phase - 1

            for y in range(3):
                for x in range(3):
                    if self.board[z][y][x] is None:
                        empty_count += 1

            if random.random() < 1 / empty_count:
                self.end_phase_by_player()
                print(f"Player:{player}", "end phase")
                return "end"

        # 駒を置く
        move = random.choice(moves)

        x, y, piece, direction1, direction2 = move

        self.put_piece(
            x, y, piece, direction1, direction2
        )

        print(
            f'Player:{player}',
            'put',
            f'({x}, {y})',
            f'{piece.color1}{piece.color2}',
            f'{direction1}{direction2}',
            f'--{len(self.hand[self.current_player])}')

        return "put"