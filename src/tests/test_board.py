import unittest
from src.board_utils import (
    generate_initial_board,
    print_board,
    generate_legal_moves,
    make_move
)

class TestBoard(unittest.TestCase):
    def setUp(self):
        # Set up the initial board before each test
        self.board = generate_initial_board()

    def test_initial_board_setup(self):
        # Check that the initial setup of the board is correct

        # Black pieces in the first row
        expected_first_row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        self.assertEqual(self.board[0], expected_first_row)

        # White pieces in the last row
        expected_last_row = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.assertEqual(self.board[7], expected_last_row)

        # Check black and white pawns
        self.assertEqual(self.board[1], ['p'] * 8)
        self.assertEqual(self.board[6], ['P'] * 8)

        # Check that rows 2 to 5 are empty
        for row in range(2, 6):
            self.assertEqual(self.board[row], ['.'] * 8)

    def test_print_board(self):
        # Just ensure that the print_board function runs without error
        # It will print the board to the console
        print_board(self.board)

    def test_generate_legal_moves_initial_white(self):
        # At the start of the game, white should have some legal moves
        moves = generate_legal_moves(self.board, "white")
        self.assertTrue(len(moves) > 0, "White should have some legal moves at the start.")

    def test_make_move(self):
        # Test making a move: move a white pawn from (6,0) to (4,0)
        start_pos = (6, 0)
        end_pos = (4, 0)
        updated_board = make_move(self.board, start_pos, end_pos)

        # Check that the piece moved correctly
        self.assertEqual(updated_board[4][0], 'P')
        self.assertEqual(updated_board[6][0], '.')

if __name__ == '__main__':
    unittest.main()
