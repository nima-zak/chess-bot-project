import unittest
import chess
from src.engine import Engine

class TestEngine(unittest.TestCase):

    def test_evaluate_board(self):
        fen = "8/8/8/8/8/8/8/4K2Q w - - 0 1"
        board = chess.Board(fen=fen)
        engine = Engine(color_is_white=True)
        score = engine.evaluate_board(board)
        self.assertGreater(score, 8.0)

        engine_black = Engine(color_is_white=False)
        score_black = engine_black.evaluate_board(board)
        self.assertLess(score_black, -8.0)

    def test_find_best_move_initial_position(self):
        board = chess.Board()
        engine = Engine(color_is_white=True)
        move = engine.find_best_move(board, depth=1)
        self.assertIsNotNone(move)
        self.assertIn(move, board.legal_moves)

    def test_mate_in_one(self):
        # Position with only one legal move which is mate in one:
        fen = "6Pk/6pQ/6pp/8/8/8/8/K7 w - - 0 1"
        board = chess.Board(fen=fen)
        engine = Engine(color_is_white=True)
        best_move = engine.find_best_move(board, depth=4)
        self.assertIsNotNone(best_move)
        self.assertEqual(best_move.uci(), "h7h8", "Engine should find the checkmate move Qh7-h8")

    def test_engine_as_black(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
        board = chess.Board(fen=fen)
        engine_black = Engine(color_is_white=False)
        move = engine_black.find_best_move(board, depth=1)
        self.assertIsNotNone(move)
        self.assertIn(move, board.legal_moves)

if __name__ == '__main__':
    unittest.main()
