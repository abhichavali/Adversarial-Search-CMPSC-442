SIZE = 6


def read_state(filename="input.txt"):
    values = []
    with open(filename) as f:
        for line in f:
            if line.strip() == "":
                continue
            values.append([int(x.strip()) for x in line.split(",")])

    if len(values) != SIZE:
        raise ValueError("The board must have 6 rows with 6 numbers in each row.")
    for row in values:
        if len(row) != SIZE:
            raise ValueError("The board must have 6 rows with 6 numbers in each row.")
        for x in row:
            if x < 1 or x > 99:
                raise ValueError("Tile values must be between 1 and 99.")

    board = []
    for i in range(SIZE):
        board.append([None] * SIZE)
    return (values, board, "Alpha")


def neighbors(row, col):
    near = []
    if row > 0:
        near.append((row - 1, col))
    if row < SIZE - 1:
        near.append((row + 1, col))
    if col > 0:
        near.append((row, col - 1))
    if col < SIZE - 1:
        near.append((row, col + 1))
    return near

def all_possible_options(state):
    board = state[1]
    team = state[2]
    moves = []

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] is not None:
                continue

            moves.append(("Deploy", row, col))
            for r, c in neighbors(row, col):
                if board[r][c] == team:
                    moves.append(("Assault", row, col))
                    break
    return moves

def legal_moves(state):
    possible_moves = all_possible_options(state)
    captures = []
    board = state[1]
    other = "Bravo" if state[2] == "Alpha" else "Alpha"

    for move in possible_moves:
        action, row, col = move
        if action == "Assault":
            for r, c in neighbors(row, col):
                if board[r][c] == other:
                    captures.append(move)
                    break

    # Have to capture if there is a move that can do it.
    if len(captures) > 0:
        return captures
    return possible_moves


def apply_move(state, move):
    if move not in legal_moves(state):
        raise ValueError("Illegal move.")

    save_state = list(state)
    # Copy each row so the old board does not change.
    save_state[1] = [row.copy() for row in state[1]]
    action, row, col = move
    team = state[2]
    save_state[2] = "Bravo" if team == "Alpha" else "Alpha"

    save_state[1][row][col] = team
    if action == "Assault":
        for r, c in neighbors(row, col):
            if save_state[1][r][c] == save_state[2]:
                save_state[1][r][c] = team

    return tuple(save_state)

def scores(state):
    values, board, _ = state
    a = 0
    b = 0
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == "Alpha":
                a += values[row][col]
            if board[row][col] == "Bravo":
                b += values[row][col]
    return (a, b)


def is_gameover(state):
    board = state[1]
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] is None:
                return False
    return True

def winner(state):
    if not is_gameover(state):
        return None

    a, b = scores(state)
    if a > b:
        return "Alpha"
    if b > a:
        return "Bravo"
    return "Draw"


def print_board(state):
    values, board, _ = state
    text = "<"
    for row in range(SIZE):
        for col in range(SIZE):
            text += str(values[row][col])
            if board[row][col] == "Alpha":
                text += "A"
            elif board[row][col] == "Bravo":
                text += "B"
            else:
                text += "."
            if col < SIZE - 1:
                text += ","
        if row < SIZE - 1:
            text += "\n"
    print(text + ">")


def choose_move(state):
    # First move for now, search is not added yet.
    moves = legal_moves(state)
    if len(moves) == 0:
        return None
    return moves[0]

def report(number, team, move, state):
    action, row, col = move
    letters = ["A", "B", "C", "D", "E", "F"]
    column = letters[col]

    print(f"Move {number}:")
    print(f"Action for team: <Team-{team}>")
    print(f"{action}: [{column},{row + 1}]")
    print_board(state)
    a, b = scores(state)
    print(f"Total score - Alpha: {a}")
    print(f"Total score - Bravo: {b}")
    print()


def main():
    try:
        cur_state = read_state()
    except Exception as e:
        print("Could not load input.txt: " + str(e))
        return

    print("Board marks: A = Alpha, B = Bravo, . = unclaimed\n")
    count = 1
    while not is_gameover(cur_state):
        team = cur_state[2]
        move = choose_move(cur_state)
        cur_state = apply_move(cur_state, move)
        report(count, team, move, cur_state)
        count += 1

    result = winner(cur_state)
    if result == "Draw":
        print("The Winner is: <Draw>")
    else:
        print(f"The Winner is: <Team-{result}>")


if __name__ == "__main__":
    main()
