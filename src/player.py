import time
from src.rules import Rules
from src.engine import Engine

class Player:
    """
    The Player class represents either a human or a bot player.
    It uses the Rules class to apply moves and, if it's a bot,
    it interacts with the Engine to decide the best move.
    It also manages time and stores search statistics.
    """

    def __init__(self, name, player_type, color, rules=None, time_limit=600.0):
        """
        Initialize a Player instance.

        Args:
            name (str): The player's name.
            player_type (str): "human" or "bot".
            color (str): "white" or "black".
            rules (Rules): A Rules object managing the board. If None, a new one is created.
            time_limit (float): The initial time in seconds for this player.
        """
        self.name = name
        self.player_type = player_type
        self.color = color
        self.rules = rules if rules else Rules()
        self.moves_history = []
        self.time_left = time_limit
        self._timer_start = None

        if self.player_type == "bot":
            color_is_white = (self.color == "white")
            self.engine = Engine(color_is_white=color_is_white)
        else:
            self.engine = None

        # Store move statistics: list of dicts with "move", "time_taken", "depth", "nodes_searched"
        self.move_statistics = []

    def start_timer(self):
        """Start timing the current move."""
        self._timer_start = time.time()

    def stop_timer(self):
        """Stop timing and update remaining time."""
        if self._timer_start is not None:
            elapsed = time.time() - self._timer_start
            self.time_left -= elapsed
            self._timer_start = None

    def _choose_depth_based_on_time(self):
        """
        Choose search depth based on remaining time:
            - time < 5s => depth = 1
            - 5s <= time <= 30s => depth = 2
            - 30s < time <= 100s => depth = 3
            - time > 100s => depth = 4

        Returns:
            int: The chosen depth.
        """
        if self.time_left < 5:
            return 1
        elif self.time_left <= 30:
            return 2
        elif self.time_left <= 100:
            return 3
        else:
            return 4

    def make_move(self, move_uci=None):
        """
        Make a move on the board.
        If human, move_uci must be provided and legal.
        If bot, choose best move using the engine.

        Returns:
            bool: True if a move was made, False otherwise.
        """
        self.start_timer()

        board_color_turn = 'white' if self.rules.board.turn else 'black'
        if board_color_turn != self.color:
            self.stop_timer()
            raise ValueError(f"It's not {self.color}'s turn to move.")

        if self.player_type == "human":
            if move_uci is None:
                self.stop_timer()
                raise ValueError("No move provided for a human player.")
            success = self.rules.apply_move(move_uci)
            if success:
                self.moves_history.append(move_uci)
            self.stop_timer()
            return success
        else:
            # Bot player
            depth = self._choose_depth_based_on_time()
            # We'll allow engine the remaining time for iterative deepening
            time_for_move = self.time_left  # Engine can use all remaining time for this move if needed

            best_move, nodes, search_time = self.engine.find_best_move_with_stats(self.rules.board, depth, time_for_move)

            if best_move is None:
                # No moves found or game over
                self.stop_timer()
                return False

            self.rules.board.push(best_move)
            self.moves_history.append(best_move.uci())

            # Store stats: time taken for this move is (start->stop_timer), nodes searched, depth used
            elapsed = (time.time() - (time.time() - self.time_left)) if self._timer_start is None else 0.0
            # Actually, we have better approach:
            # We know stop_timer will recalc time_left, so let's just measure after stop_timer
            self.stop_timer()
            move_time = self.time_left if self._timer_start is None else 0.0
            # Actually, to get the exact move_time, we should do:
            # We started timer at self._timer_start, we can do:
            move_time = 0.0
            if self._timer_start is not None:
                elapsed_now = time.time() - self._timer_start
                move_time = elapsed_now
            else:
                # If we ended timer above, we must recalculate
                move_time = search_time

            self.move_statistics.append({
                "move": best_move.uci(),
                "time_taken": move_time,
                "depth_used": depth,
                "nodes_searched": nodes
            })

            return True

    def get_moves_history(self):
        """Return the moves made by this player."""
        return self.moves_history

    def get_move_statistics(self):
        """
        Return the statistics of moves made by this player, including:
        - Time taken per move
        - Depth used
        - Nodes searched
        """
        return self.move_statistics
