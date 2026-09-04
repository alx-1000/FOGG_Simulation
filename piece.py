#color
R = "R"
B = "B"
T = "T"
N = "N"


class Piece:
    def __init__(self, owner, color1, color2):
        self.owner = owner
        self.color1 = color1
        self.color2 = color2
        self.direction1 = None
        self.direction2 = None

def make_pieces(owner, color1, color2, count):
    return [
        Piece(owner, color1, color2)
        for _ in range(count)
    ]

pieces_F = (
    make_pieces("F", R, B, 3) +
    make_pieces("F", R, T, 3) +
    make_pieces("F", R, R, 2) +
    make_pieces("F", R, N, 2) +
    make_pieces("F", N, N, 1) +
    make_pieces("F", N, T, 1)
)

pieces_G = (
    make_pieces("G", B, R, 3) +
    make_pieces("G", B, T, 3) +
    make_pieces("G", B, B, 2) +
    make_pieces("G", B, N, 2) +
    make_pieces("G", N, N, 1) +
    make_pieces("G", N, T, 1)
)