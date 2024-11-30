
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
