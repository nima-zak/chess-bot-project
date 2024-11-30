import unittest
from unittest.mock import patch
from io import StringIO
from src.board_utils import generate_initial_board, print_board

class TestBoardUtils(unittest.TestCase):
    def test_generate_initial_board(self):
        """
        Test that the initial board is generated correctly.
        """
        expected_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  # Black pieces
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # Black pawns
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty row
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # White pawns
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # White pieces
        ]
        generated_board = generate_initial_board()
        self.assertEqual(generated_board, expected_board)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_board(self, mock_stdout):
        """
        Test the print_board function by capturing its output.
        """
        # Board to print
        test_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        # Call the print_board function
        print_board(test_board)

        # Capture the output
        expected_output = (
            "r n b q k b n r\n"
            "p p p p p p p p\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            "P P P P P P P P\n"
            "R N B Q K B N R\n\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()


    def test_generate_pawn_moves():
        """
        Test the generate_pawn_moves function with predefined board states.
        """
        # Example board
        board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]
        # White pawn at (6, 0)
        moves = generate_pawn_moves(board, (6, 0), 'white')
        assert moves == [(5, 0), (4, 0)]  # Pawn can move one or two squares forward

        # Black pawn at (1, 0)
        board[6][0] = ' '
        board[1][0] = 'p'
        moves = generate_pawn_moves(board, (1, 0), 'black')
        assert moves == [(2, 0), (3, 0)]  # Pawn can move one or two squares forward

        # Capture diagonally
        board[2][1] = 'P'
        moves = generate_pawn_moves(board, (1, 0), 'black')
        assert moves == [(2, 0), (3, 0), (2, 1)]  # Capture possible diagonally

        print("All tests passed!")


    # Run the tests
    test_generate_pawn_moves()


    def test_generate_rook_moves():
        """
        Test the generate_rook_moves function with predefined board states.
        """
        # Example board
        board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'R', '.', '.', '.', '.'],  # White rook at (3, 3)
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
        ]

        # White rook at (3, 3)
        moves = generate_rook_moves(board, (3, 3), 'white')
        expected_moves = [
            (2, 3), (1, 3), (0, 3),  # Up
            (4, 3), (5, 3), (6, 3), (7, 3),  # Down
            (3, 2), (3, 1), (3, 0),  # Left
            (3, 4), (3, 5), (3, 6), (3, 7)  # Right
        ]
        assert sorted(moves) == sorted(expected_moves)

        # Test with obstacles
        board[1][3] = 'p'  # Black pawn blocking upward
        board[5][3] = 'P'  # White pawn blocking downward
        moves = generate_rook_moves(board, (3, 3), 'white')
        expected_moves = [
            (2, 3),  # Up until obstacle
            (4, 3),  # Down until obstacle
            (3, 2), (3, 1), (3, 0),  # Left
            (3, 4), (3, 5), (3, 6), (3, 7)  # Right
        ]
        assert sorted(moves) == sorted(expected_moves)

        print("All tests for generate_rook_moves passed!")

def test_generate_knight_moves():
    """
    Test the generate_knight_moves function with predefined board states.
    """
    # Example board
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'N', '.', '.', '.', '.'],  # White knight at (3, 3)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ]

    # White knight at (3, 3)
    moves = generate_knight_moves(board, (3, 3), 'white')
    expected_moves = [
        (5, 4), (5, 2), (1, 4), (1, 2),  # L-shape moves
        (4, 5), (4, 1), (2, 5), (2, 1)
    ]
    assert sorted(moves) == sorted(expected_moves)

    # Test with obstacles
    board[5][4] = 'p'  # Black pawn (can capture)
    board[1][4] = 'P'  # White pawn (cannot capture)
    moves = generate_knight_moves(board, (3, 3), 'white')
    expected_moves = [
        (5, 4), (5, 2), (1, 2),  # Adjusted moves
        (4, 5), (4, 1), (2, 5), (2, 1)
    ]
    assert sorted(moves) == sorted(expected_moves)

    print("All tests for generate_knight_moves passed!")

def test_generate_bishop_moves():
    """
    Test the generate_bishop_moves function with predefined board states.
    """
    # Example board
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', '.', '.', '.', '.'],  # White bishop at (3, 3)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ]

    # White bishop at (3, 3)
    moves = generate_bishop_moves(board, (3, 3), 'white')
    expected_moves = [
        (4, 4), (5, 5), (6, 6), (7, 7),  # Down-right
        (4, 2), (5, 1), (6, 0),         # Down-left
        (2, 4), (1, 5), (0, 6),         # Up-right
        (2, 2), (1, 1), (0, 0)          # Up-left
    ]
    assert sorted(moves) == sorted(expected_moves)

    # Test with obstacles
    board[5][5] = 'p'  # Black pawn (can capture)
    board[2][2] = 'P'  # White pawn (cannot capture)
    moves = generate_bishop_moves(board, (3, 3), 'white')
    expected_moves = [
        (4, 4), (5, 5),  # Down-right (stops at black pawn)
        (4, 2), (5, 1), (6, 0),  # Down-left
        (2, 4), (1, 5), (0, 6),  # Up-right
        (2, 2)                   # Up-left (stops before white pawn)
    ]
    assert sorted(moves) == sorted(expected_moves)

    print("All tests for generate_bishop_moves passed!")

def test_generate_queen_moves():
    """
    Test the generate_queen_moves function with predefined board states.
    """
    # Example board
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'Q', '.', '.', '.', '.'],  # White queen at (3, 3)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ]

    # White queen at (3, 3)
    moves = generate_queen_moves(board, (3, 3), 'white')
    expected_moves = [
        # Rook-like moves
        (2, 3), (1, 3), (0, 3), (4, 3), (5, 3), (6, 3), (7, 3),  # Vertical
        (3, 2), (3, 1), (3, 0), (3, 4), (3, 5), (3, 6), (3, 7),  # Horizontal
        # Bishop-like moves
        (4, 4), (5, 5), (6, 6), (7, 7),  # Down-right
        (4, 2), (5, 1), (6, 0),         # Down-left
        (2, 4), (1, 5), (0, 6),         # Up-right
        (2, 2), (1, 1), (0, 0)          # Up-left
    ]
    assert sorted(moves) == sorted(expected_moves)

    # Test with obstacles
    board[5][5] = 'p'  # Black pawn (can capture)
    board[2][3] = 'P'  # White pawn (cannot capture)
    moves = generate_queen_moves(board, (3, 3), 'white')
    expected_moves = [
        # Adjusted rook-like moves
        (4, 3), (5, 3), (6, 3), (7, 3),
        (3, 2), (3, 1), (3, 0), (3, 4), (3, 5), (3, 6), (3, 7),
        # Adjusted bishop-like moves
        (4, 4), (5, 5),  # Stops at black pawn
        (4, 2), (5, 1), (6, 0),
        (2, 4), (1, 5), (0, 6),
        (2, 2)  # Stops before white pawn
    ]
    assert sorted(moves) == sorted(expected_moves)

    print("All tests for generate_queen_moves passed!")

def test_generate_king_moves():
    """
    Test the generate_king_moves function with predefined board states.
    """
    # Example board
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'K', '.', '.', '.', '.'],  # White king at (3, 3)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ]

    # White king at (3, 3)
    moves = generate_king_moves(board, (3, 3), 'white')
    expected_moves = [
        (2, 2), (2, 3), (2, 4),  # Top-left, Top, Top-right
        (3, 2),          (3, 4),  # Left, Right
        (4, 2), (4, 3), (4, 4)   # Bottom-left, Bottom, Bottom-right
    ]
    assert sorted(moves) == sorted(expected_moves)

    # Test with obstacles
    board[4][4] = 'p'  # Black pawn (can capture)
    board[3][2] = 'P'  # White pawn (cannot capture)
    moves = generate_king_moves(board, (3, 3), 'white')
    expected_moves = [
        (2, 2), (2, 3), (2, 4),
        (3, 4),  # Right
        (4, 2), (4, 3), (4, 4)  # Bottom-right (can capture black pawn)
    ]
    assert sorted(moves) == sorted(expected_moves)

    print("All tests for generate_king_moves passed!")

