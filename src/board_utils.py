def generate_initial_board():
    """
    Generates the initial chess board as a 2D list.
    Returns:
        list: A 2D list representing the initial chess board.
    """
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  # Black pieces (row 0)
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # Black pawns (row 1)
        ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row (row 2)
        ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row (row 3)
        ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row (row 4)
        ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row (row 5)
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # White pawns (row 6)
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # White pieces (row 7)
    ]
    return board

def print_board(board):
    """
    Prints the chess board in a human-readable format.
    Args:
        board (list): The 2D list representing the chess board.
    """
    for row in board:
        print(' '.join(row))
    print()

def generate_pawn_moves(board, position, player):
    moves = []
    row, col = position
    direction = -1 if player == "white" else 1  # White moves up, Black moves down

    # Move forward one square
    if 0 <= row + direction < 8 and board[row + direction][col] == '.':
        moves.append((row + direction, col))

        # Move forward two squares if the pawn is in its starting position
        if (player == "white" and row == 6) or (player == "black" and row == 1):
            if board[row + 2 * direction][col] == '.':
                moves.append((row + 2 * direction, col))

    # Capture diagonally
    if player == "white":
        # Capture to the left
        if 0 <= row + direction < 8 and 0 <= col - 1 < 8 and board[row + direction][col - 1].islower():
            moves.append((row + direction, col - 1))
        # Capture to the right
        if 0 <= row + direction < 8 and 0 <= col + 1 < 8 and board[row + direction][col + 1].islower():
            moves.append((row + direction, col + 1))
    else:  # player == "black"
        # Capture to the left
        if 0 <= row + direction < 8 and 0 <= col - 1 < 8 and board[row + direction][col - 1].isupper():
            moves.append((row + direction, col - 1))
        # Capture to the right
        if 0 <= row + direction < 8 and 0 <= col + 1 < 8 and board[row + direction][col + 1].isupper():
            moves.append((row + direction, col + 1))

    return moves

def generate_rook_moves(board, position, player):
    moves = []
    row, col = position
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dr, dc in directions:
        r, c = row, col
        while True:
            r += dr
            c += dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '.':
                    moves.append((r, c))
                elif (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()):
                    moves.append((r, c))
                    break
                else:
                    break
            else:
                break
    return moves

def generate_knight_moves(board, position, player):
    moves = []
    row, col = position
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == '.' or (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()):
                moves.append((r, c))
    return moves

def generate_bishop_moves(board, position, player):
    moves = []
    row, col = position
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in directions:
        r, c = row, col
        while True:
            r += dr
            c += dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == '.':
                    moves.append((r, c))
                elif (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()):
                    moves.append((r, c))
                    break
                else:
                    break
            else:
                break
    return moves

def generate_queen_moves(board, position, player):
    rook_moves_list = generate_rook_moves(board, position, player)
    bishop_moves_list = generate_bishop_moves(board, position, player)
    return rook_moves_list + bishop_moves_list

def generate_king_moves(board, position, player):
    moves = []
    row, col = position
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == '.' or (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()):
                moves.append((r, c))
    return moves

def generate_legal_moves(board, player):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (player == "white" and piece.isupper()) or (player == "black" and piece.islower()):
                position = (row, col)
                if piece.lower() == 'p':
                    piece_moves = generate_pawn_moves(board, position, player)
                elif piece.lower() == 'r':
                    piece_moves = generate_rook_moves(board, position, player)
                elif piece.lower() == 'n':
                    piece_moves = generate_knight_moves(board, position, player)
                elif piece.lower() == 'b':
                    piece_moves = generate_bishop_moves(board, position, player)
                elif piece.lower() == 'q':
                    piece_moves = generate_queen_moves(board, position, player)
                elif piece.lower() == 'k':
                    piece_moves = generate_king_moves(board, position, player)
                else:
                    piece_moves = []

                for move in piece_moves:
                    moves.append((position, move))
    return moves

def make_move(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = '.'  # Empty the starting position
    return board

if __name__ == "__main__":
    # This block is only for direct testing of this file
    chess_board = generate_initial_board()
    print_board(chess_board)
    moves = generate_legal_moves(chess_board, "white")
    print("White's initial moves:")
    print(moves)
