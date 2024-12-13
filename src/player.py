# src/player.py
from src.rules import Rules

class Player:
    def __init__(self, name, player_type, color, rules=None):
        self.name = name
        self.player_type = player_type
        self.color = color
        self.rules = rules if rules else Rules()
        self.moves_history = []

    def make_move(self, move_uci):
        board_color_turn = 'white' if self.rules.board.turn else 'black'
        if board_color_turn != self.color:
            raise ValueError(f"It's not {self.color}'s turn to move.")

        if self.rules.apply_move(move_uci):
            self.moves_history.append(move_uci)
            return True
        return False

    def get_moves_history(self):
        return self.moves_history
