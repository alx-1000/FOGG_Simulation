def print_piece(piece):
    if piece is None:
        return [
            "   ",
            "   ",
            " - "
        ]

    directions = {
        "X": "□",
        "Y": "□",
        "Z": "□"
    }

    directions[piece.direction1] = piece.color1
    directions[piece.direction2] = piece.color2

    x = directions["X"]
    y = directions["Y"]
    z = directions["Z"]

    return [
        f"{y}",
        "│ ",
        f"{z}──{x}"
    ]


def print_board(board):

    CELL_WIDTH = 12

    print(
        f"{'z=0':^{CELL_WIDTH * 3}}"
        f"{'z=1':^{CELL_WIDTH * 3}}"
        f"{'z=2':^{CELL_WIDTH * 3}}"
    )

    for y in range(3):

        lines = ["", "", ""]

        for z in range(3):

            for x in range(3):

                piece = board[z][y][x]

                if piece is None:

                    piece_lines = [
                        " " * CELL_WIDTH,
                        " " * CELL_WIDTH,
                        f"{'-':^{CELL_WIDTH}}"
                    ]

                else:

                    directions = {
                        "X": "□",
                        "Y": "□",
                        "Z": "□"
                    }

                    directions[piece.direction1] = piece.color1
                    directions[piece.direction2] = piece.color2

                    x_char = directions["X"]
                    y_char = directions["Y"]
                    z_char = directions["Z"]

                    piece_lines = [
                        f"{y_char:^{CELL_WIDTH}}",
                        f"{'│':^{CELL_WIDTH}}",
                        f"{z_char + '──' + x_char:^{CELL_WIDTH}}"
                    ]

                for i in range(3):
                    lines[i] += piece_lines[i]

        for line in lines:
            print(line)

        print()