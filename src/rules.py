# src/rules.py
import chess

class Rules:
    def __init__(self, fen=None):
        if fen:
            self.board = chess.Board(fen=fen)
        else:
            self.board = chess.Board()

    def is_move_legal(self, move_uci):
        try:
            move = self.board.parse_uci(move_uci)
        except ValueError:
            return False
        return move in self.board.legal_moves

    def apply_move(self, move_uci):
        if not self.is_move_legal(move_uci):
            return False
        move = self.board.parse_uci(move_uci)
        self.board.push(move)
        return True

    def is_in_check(self, color='white'):
        desired_color = (color == 'white')
        original_turn = self.board.turn
        self.board.turn = desired_color
        in_check = self.board.is_check()
        self.board.turn = original_turn
        return in_check

    def is_checkmate(self, color='white'):
        desired_color = (color == 'white')
        original_turn = self.board.turn
        self.board.turn = desired_color
        checkmate = self.board.is_checkmate()
        self.board.turn = original_turn
        return checkmate

    def is_stalemate(self, color='white'):
        desired_color = (color == 'white')
        original_turn = self.board.turn
        self.board.turn = desired_color
        stalemate = self.board.is_stalemate()
        self.board.turn = original_turn
        return stalemate

    def is_fifty_move_rule(self):
        return self.board.halfmove_clock >= 100

    def is_threefold_repetition(self):
        return self.board.is_repetition(3)

    def can_claim_draw(self):
        return self.board.can_claim_draw()

    def legal_moves_list(self):
        return [move.uci() for move in self.board.legal_moves]

    def set_fen(self, fen):
        self.board.set_fen(fen)

    def get_fen(self):
        return self.board.fen()

    def is_insufficient_material(self):
        return self.board.is_insufficient_material()

    def is_game_over(self):
        return self.board.is_game_over()

    def result(self):
        return self.board.result()
