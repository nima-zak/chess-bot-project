import time
from src.rules import Rules
from src.engine import Engine
import chess


class Player:
    """
    The Player class represents a chess player, which can be a human or a bot.
    It manages:
    - Move application via the Rules class.
    - For a bot player, it uses the Engine to determine the best move.
    - Time management: starts and stops a timer for each move, and adjusts strategy if time is low.

    Attributes:
        name (str): Player's name.
        player_type (str): "human" or "bot".
        color (str): "white" or "black".
        rules (Rules): An instance of Rules to manage board and move legality.
        moves_history (list): A list of UCI moves played by this player.
        time_left (float): Remaining time in seconds for this player.
        _timer_start (float or None): Time at which the current move started.
        engine (Engine or None): If player_type is "bot", an Engine instance is used to select moves.
    """

    def __init__(self, name, player_type, color, rules=None, time_limit=600):
        """
        Initialize a Player instance.

        Args:
            name (str): The name of the player.
            player_type (str): Either "human" or "bot".
            color (str): "white" or "black".
            rules (Rules): A Rules object for managing the board state. If None, a new Rules instance is created.
            time_limit (int or float): Initial time limit for the player in seconds.
        """
        self.name = name
        self.player_type = player_type
        self.color = color
        self.rules = rules if rules else Rules()
        self.moves_history = []
        self.time_left = time_limit
        self._timer_start = None

        # If bot, initialize an engine for decision making
        if self.player_type == "bot":
            color_is_white = (self.color == "white")
            self.engine = Engine(color_is_white=color_is_white)
        else:
            self.engine = None

    def start_timer(self):
        """
        Start the move timer for this player.
        This should be called at the beginning of a move.
        """
        self._timer_start = time.time()

    def stop_timer(self):
        """
        Stop the move timer and update the player's remaining time.
        """
        if self._timer_start is not None:
            elapsed = time.time() - self._timer_start
            self.time_left -= elapsed
            self._timer_start = None

    def make_move(self, move_uci=None):
        """
        Make a move on the board.

        For a human player, move_uci must be provided.
        For a bot player:
            - If move_uci is provided, it will be ignored.
            - The Engine will be used to find the best move.

        This method also considers time management:
        - If time is low, reduce the search depth to ensure a faster decision.

        Args:
            move_uci (str or None): The UCI move string for a human player's move, or None for a bot.

        Returns:
            bool: True if the move was successfully made, False otherwise.
        """
        self.start_timer()

        board_color_turn = 'white' if self.rules.board.turn else 'black'
        if board_color_turn != self.color:
            self.stop_timer()
            raise ValueError(f"It's not {self.color}'s turn to move.")

        if self.player_type == "human":
            # For a human player, the move_uci must be given and legal.
            if move_uci is None:
                self.stop_timer()
                raise ValueError("No move provided for a human player.")
            success = self.rules.apply_move(move_uci)
            if success:
                self.moves_history.append(move_uci)
            self.stop_timer()
            return success
        else:
            # Bot player: decide the move using the engine.
            # Adjust search depth based on remaining time.
            depth = self._choose_depth_based_on_time()

            best_move = self.engine.find_best_move(self.rules.board, depth)
            if best_move is None:
                # No moves available (likely game over)
                self.stop_timer()
                return False

            self.rules.board.push(best_move)
            self.moves_history.append(best_move.uci())
            self.stop_timer()
            return True

    def _choose_depth_based_on_time(self):
        """
        Choose the search depth based on the remaining time.
        If time is running low, reduce depth for faster moves.

        This is a simple heuristic. You can make it more sophisticated:
        - If time < 30 seconds: depth = 2
        - If time < 10 seconds: depth = 1
        - Otherwise: depth = 3

        Returns:
            int: The chosen search depth.
        """
        if self.time_left < 10:
            return 1
        elif self.time_left < 30:
            return 2
        else:
            return 3

    def get_moves_history(self):
        """
        Get the list of moves made by this player.

        Returns:
            list: The moves made by this player as UCI strings.
        """
        return self.moves_history
