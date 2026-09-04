def calculate_colors(colors):
    if "N" in colors:
        return "N"

    if "R" in colors and "B" in colors:
        return "N"

    if "R" in colors:
        return "R"

    if "B" in colors:
        return "B"

    return "T"

def get_color(piece, direction):
    if piece is None:
        return "T"

    if piece.direction1 == direction:
        return piece.color1

    if piece.direction2 == direction:
        return piece.color2

    return "T"


def calculate_x_lines(board, phase):
    results = []

    for z in range(phase):
        for y in range(3):

            colors = []

            for x in range(3):
                piece = board[z][y][x]
                colors.append(get_color(piece, "X"))

            result = calculate_colors(colors)
            results.append(result)

    return results

def calculate_y_lines(board, phase):
    results = []

    for z in range(phase):
        for x in range(3):
            colors = []

            for y in range(3):
                piece = board[z][y][x]
                colors.append(get_color(piece, "Y"))

            result = calculate_colors(colors)
            results.append(result)

    return results

def calculate_z_lines(board, phase):
    results = []

    for y in range(3):
        for x in range(3):
            colors = []

            for z in range(phase):
                piece = board[z][y][x]
                colors.append(get_color(piece, "Z"))

            result = calculate_colors(colors)
            results.append(result)

    return results

def calculate_score(x_lines, y_lines, z_lines):
    score_F = 0
    score_G = 0

    for result in x_lines:
        if result == "R":
            score_F += 1
        elif result == "B":
            score_G += 1

    for result in y_lines:
        if result == "R":
            score_F += 1
        elif result == "B":
            score_G += 1

    for result in z_lines:
        if result == "R":
            score_F += 1
        elif result == "B":
            score_G += 1

    return score_F, score_G

##デバッグ
assert calculate_colors(["R"]) == "R"
assert calculate_colors(["B"]) == "B"
assert calculate_colors(["T"]) == "T"
assert calculate_colors(["N"]) == "N"

assert calculate_colors(["R", "T"]) == "R"
assert calculate_colors(["B", "T"]) == "B"
assert calculate_colors(["R", "B"]) == "N"

assert calculate_colors(["R", "T", "T"]) == "R"
assert calculate_colors(["B", "T", "T"]) == "B"
assert calculate_colors(["R", "B", "T"]) == "N"
assert calculate_colors(["N", "R", "T"]) == "N"