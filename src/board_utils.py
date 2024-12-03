
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

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Generate the initial board
    chess_board = generate_initial_board()
    # Print the board
    print_board(chess_board)


    def generate_legal_moves(board, player):
        """
        Generate all legal moves for a given player.

        Args:
            board (list): The 8x8 chess board represented as a matrix.
            player (str): The player ("white" or "black").

        Returns:
            list: A list of all legal moves as ((start_row, start_col), (end_row, end_col)).
        """
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if (player == "white" and piece.isupper()) or (player == "black" and piece.islower()):
                    position = (row, col)

                    # Determine the moves based on the piece type
                    if piece.lower() == 'p':  # Pawn
                        piece_moves = generate_pawn_moves(board, position, player)
                    elif piece.lower() == 'r':  # Rook
                        piece_moves = generate_rook_moves(board, position, player)
                    elif piece.lower() == 'n':  # Knight
                        piece_moves = generate_knight_moves(board, position, player)
                    elif piece.lower() == 'b':  # Bishop
                        piece_moves = generate_bishop_moves(board, position, player)
                    elif piece.lower() == 'q':  # Queen
                        piece_moves = generate_queen_moves(board, position, player)
                    elif piece.lower() == 'k':  # King
                        piece_moves = generate_king_moves(board, position, player)
                    else:
                        piece_moves = []

                    # Add moves to the list as ((start_row, start_col), (end_row, end_col))
                    for move in piece_moves:
                        moves.append((position, move))
        return moves




    # Function to generate legal moves for a pawn
    def generate_pawn_moves(board, position, player):
        """
        Generate legal moves for a pawn based on its position and the current board state.

        Args:
            board (list): The 8x8 chess board represented as a matrix.
            position (tuple): The (row, col) position of the pawn on the board.
            player (str): The player ("white" or "black").

        Returns:
            list: A list of legal moves as (row, col) tuples.
        """
        moves = []
        row, col = position
        direction = -1 if player == "white" else 1  # White moves up, Black moves down

        # Move forward one square
        if 0 <= row + direction < 8 and board[row + direction][col] == ' ':
            moves.append((row + direction, col))

            # Move forward two squares if the pawn is in its starting position
            if (player == "white" and row == 6) or (player == "black" and row == 1):
                if board[row + 2 * direction][col] == ' ':
                    moves.append((row + 2 * direction, col))

        # Capture diagonally to the left
        if 0 <= col - 1 < 8 and 0 <= row + direction < 8:
            if board[row + direction][col - 1].islower() if player == "white" else board[row + direction][
                col - 1].isupper():
                moves.append((row + direction, col - 1))

        # Capture diagonally to the right
        if 0 <= col + 1 < 8 and 0 <= row + direction < 8:
            if board[row + direction][col + 1].islower() if player == "white" else board[row + direction][
                col + 1].isupper():
                moves.append((row + direction, col + 1))

        return moves


    # Function to generate legal moves for a rook
    def generate_rook_moves(board, position, player):
        """
        Generate legal moves for a rook based on its position and the current board state.

        Args:
            board (list): The 8x8 chess board represented as a matrix.
            position (tuple): The (row, col) position of the rook on the board.
            player (str): The player ("white" or "black").

        Returns:
            list: A list of legal moves as (row, col) tuples.
        """
        moves = []
        row, col = position

        # Define the directions the rook can move: horizontal and vertical
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                # Check if the position is within bounds
                if 0 <= r < 8 and 0 <= c < 8:
                    # If the position is empty, add it to the moves
                    if board[r][c] == '.':
                        moves.append((r, c))
                    # If there's an opponent's piece, add the position and stop
                    elif (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()):
                        moves.append((r, c))
                        break
                    # If there's a piece of the same player, stop
                    else:
                        break
                else:
                    break

        return moves


    # Function to generate legal moves for a knight
    def generate_knight_moves(board, position, player):
        """
        Generate legal moves for a knight based on its position and the current board state.

        Args:
            board (list): The 8x8 chess board represented as a matrix.
            position (tuple): The (row, col) position of the knight on the board.
            player (str): The player ("white" or "black").

        Returns:
            list: A list of legal moves as (row, col) tuples.
        """
        moves = []
        row, col = position

        # All possible moves for a knight (L-shape)
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            # Check if the position is within bounds
            if 0 <= r < 8 and 0 <= c < 8:
                # Allow empty squares or opponent's pieces
                if board[r][c] == '.' or (player == "white" and board[r][c].islower()) or (
                        player == "black" and board[r][c].isupper()):
                    moves.append((r, c))

        return moves

# Function to generate legal moves for a bishop
def generate_bishop_moves(board, position, player):
    """
    Generate legal moves for a bishop based on its position and the current board state.

    Args:
        board (list): The 8x8 chess board represented as a matrix.
        position (tuple): The (row, col) position of the bishop on the board.
        player (str): The player ("white" or "black").

    Returns:
        list: A list of legal moves as (row, col) tuples.
    """
    moves = []
    row, col = position

    # Define the four diagonal directions for the bishop
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        r, c = row, col
        while True:
            r += dr
            c += dc
            # Check if the position is within bounds
            if 0 <= r < 8 and 0 <= c < 8:
                # If the position is empty, add it to the moves
                if board[r][c] == '.':
                    moves.append((r, c))
                # If there's an opponent's piece, add the position and stop
                elif (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()):
                    moves.append((r, c))
                    break
                # If there's a piece of the same player, stop
                else:
                    break
            else:
                break

    return moves



# Function to generate legal moves for a queen
def generate_queen_moves(board, position, player):
    """
    Generate legal moves for a queen based on its position and the current board state.

    Args:
        board (list): The 8x8 chess board represented as a matrix.
        position (tuple): The (row, col) position of the queen on the board.
        player (str): The player ("white" or "black").

    Returns:
        list: A list of legal moves as (row, col) tuples.
    """
    # Queen's moves are the combination of rook and bishop moves
    rook_moves = generate_rook_moves(board, position, player)
    bishop_moves = generate_bishop_moves(board, position, player)

    # Combine both lists
    return rook_moves + bishop_moves

# Function to generate legal moves for a king
def generate_king_moves(board, position, player):
    """
    Generate legal moves for a king based on its position and the current board state.

    Args:
        board (list): The 8x8 chess board represented as a matrix.
        position (tuple): The (row, col) position of the king on the board.
        player (str): The player ("white" or "black").

    Returns:
        list: A list of legal moves as (row, col) tuples.
    """
    moves = []
    row, col = position

    # All possible directions for a king (one step in any direction)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
        (0, -1),          (0, 1),   # Left, Right
        (1, -1), (1, 0), (1, 1)     # Bottom-left, Bottom, Bottom-right
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        # Check if the position is within bounds
        if 0 <= r < 8 and 0 <= c < 8:
            # Allow empty squares or opponent's pieces
            if board[r][c] == '.' or (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()):
                moves.append((r, c))

    return moves

def make_move(board, start_pos, end_pos):
    """
    Make a move on the chess board.

    Args:
        board (list): The 8x8 chess board represented as a matrix.
        start_pos (tuple): The starting position of the piece (row, col).
        end_pos (tuple): The ending position of the piece (row, col).

    Returns:
        list: The updated chess board after the move.
    """
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = '.'  # Empty the starting position
    return board


