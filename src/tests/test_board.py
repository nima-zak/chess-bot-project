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
