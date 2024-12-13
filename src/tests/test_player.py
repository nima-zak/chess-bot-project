import unittest
from src.player import Player
from src.rules import Rules

class TestPlayer(unittest.TestCase):

    def test_simple_move(self):
        rules = Rules()
        white_player = Player("Alice", "human", "white", rules=rules)
        self.assertTrue(white_player.make_move("e2e4"))
        self.assertIn("e2e4", white_player.get_moves_history())

    def test_castling(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
        rules = Rules(fen)
        white_player = Player("Alice", "human", "white", rules=rules)
        self.assertTrue(white_player.make_move("e1g1"))
        self.assertIn("e1g1", white_player.get_moves_history())

    def test_en_passant(self):
        fen = "rnbqkbnr/pppp1ppp/8/4Pp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 2"
        rules = Rules(fen)
        white_player = Player("Alice", "human", "white", rules=rules)
        self.assertTrue(white_player.make_move("e5f6"))
        self.assertIn("e5f6", white_player.get_moves_history())

    def test_pawn_promotion(self):
        fen = "6k1/7P/8/8/8/8/4K3/8 w - - 0 1"
        rules = Rules(fen)
        white_player = Player("Alice", "human", "white", rules=rules)
        self.assertTrue(white_player.make_move("h7h8q"))
        self.assertIn("h7h8q", white_player.get_moves_history())

    def test_checkmate(self):
        # Scholar's mate final position (Qxf7#)
        fen = "r1bqkb1r/pppp1Qpp/2np1n2/4p2Q/2BP4/8/PPP1PPPP/RNB1K1NR b kq - 1 4"
        rules = Rules(fen)
        self.assertTrue(rules.is_checkmate("black"))

    def test_stalemate(self):
        # Stalemate position:
        fen = "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"
        rules = Rules(fen)
        self.assertTrue(rules.is_stalemate("black"))

    def test_in_check(self):
        fen = "4k3/4Q3/8/8/8/8/8/4K3 b - - 0 1"
        rules = Rules(fen)
        self.assertTrue(rules.is_in_check("black"))
        self.assertFalse(rules.is_checkmate("black"))

if __name__ == '__main__':
    unittest.main()
