import chess
import math
import time

class Engine:
    """
    The Engine class uses Minimax with Alpha-Beta pruning, iterative deepening,
    and a transposition table to find the best move.
    It also tries to detect tactical motifs like forks, pins, and skewers to prioritize moves.
    """

    def __init__(self, color_is_white=True):
        """
        Initialize the engine.

        Args:
            color_is_white (bool): True if engine plays as White, False if Black.
        """
        self.color_is_white = color_is_white
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.25,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        self.center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]

        # Transposition table: key: board hash, value: (depth, score, flag, best_move)
        # flag: exact, lowerbound, upperbound
        self.transposition_table = {}

        # Statistics for nodes
        self.nodes_searched = 0

    def evaluate_board(self, board: chess.Board):
        """
        Evaluate the board position.
        Consider material, pawn structure, king safety, center control.
        """
        if board.is_game_over():
            if board.is_checkmate():
                return -9999 if board.turn == self.color_is_white else 9999
            return 0

        material_score = self._material_score(board)
        center_score = self._center_control_score(board)
        king_safety_score = self._king_safety_score(board)
        pawn_structure_score = self._pawn_structure_score(board)

        score = material_score + center_score + king_safety_score + pawn_structure_score

        if not self.color_is_white:
            score = -score

        return score

    def _material_score(self, board: chess.Board):
        score = 0.0
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece:
                val = self.piece_values.get(piece.piece_type, 0)
                if piece.color:
                    score += val
                else:
                    score -= val
        return score

    def _center_control_score(self, board: chess.Board):
        score = 0.0
        for sq in self.center_squares:
            p = board.piece_at(sq)
            if p:
                score += 0.1 if p.color else -0.1
        return score

    def _king_safety_score(self, board: chess.Board):
        score = 0.0
        white_king = board.king(True)
        black_king = board.king(False)

        def king_safety(pos, color):
            if pos is None:
                return 0.0
            moves = [pos + d for d in [1, -1, 8, -8, 7, -7, 9, -9] if 0 <= pos + d < 64]
            safe_squares = 0
            for m in moves:
                piece = board.piece_at(m)
                if piece is None or piece.color == color:
                    safe_squares += 1
            return safe_squares * 0.05

        score += king_safety(white_king, True)
        score -= king_safety(black_king, False)
        return score

    def _pawn_structure_score(self, board: chess.Board):
        score = 0.0
        white_pawns = [sq for sq in chess.SQUARES if board.piece_at(sq) and board.piece_at(sq).piece_type == chess.PAWN and board.piece_at(sq).color]
        black_pawns = [sq for sq in chess.SQUARES if board.piece_at(sq) and board.piece_at(sq).piece_type == chess.PAWN and not board.piece_at(sq).color]

        white_files = [chess.square_file(p) for p in white_pawns]
        black_files = [chess.square_file(p) for p in black_pawns]

        # Doubled pawns
        for f in range(8):
            w_count = white_files.count(f)
            if w_count > 1:
                score -= 0.1 * (w_count - 1)
            b_count = black_files.count(f)
            if b_count > 1:
                score += 0.1 * (b_count - 1)
        return score

    def find_best_move(self, board: chess.Board, depth: int):
        """
        Find the best move with a fixed depth search.
        (Used as a fallback if no time constraints, or for initial integration.)
        """
        # Simple call to minimax with alpha-beta
        self.nodes_searched = 0
        maximizing = (board.turn == self.color_is_white)
        score, move = self._minimax(board, depth, -math.inf, math.inf, maximizing)
        return move

    def find_best_move_with_stats(self, board: chess.Board, max_depth: int, time_limit: float):
        """
        Find the best move using iterative deepening until time runs out or max_depth is reached.
        Also return stats: nodes searched, and the time spent.

        Args:
            board (chess.Board): Current board state.
            max_depth (int): Maximum depth to search.
            time_limit (float): Time allowed for this move in seconds.

        Returns:
            (move: chess.Move, nodes: int, search_time: float)
        """
        start_time = time.time()
        self.nodes_searched = 0
        best_move = None
        best_score = -math.inf if board.turn == self.color_is_white else math.inf

        # Iterative deepening:
        for depth in range(1, max_depth + 1):
            if time.time() - start_time >= time_limit:
                break
            maximizing = (board.turn == self.color_is_white)
            score, move = self._minimax(board, depth, -math.inf, math.inf, maximizing, start_time, time_limit)
            if move is not None:
                best_move = move
                best_score = score
            if time.time() - start_time >= time_limit:
                break

        search_time = time.time() - start_time
        return best_move, self.nodes_searched, search_time

    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizingPlayer: bool, start_time=None, time_limit=None):
        """
        Minimax search with Alpha-Beta pruning and Transposition Table.
        Also uses a simple move ordering by prioritizing tactical moves.

        Args:
            board (chess.Board): The current position.
            depth (int): Current search depth.
            alpha (float): Alpha for pruning.
            beta (float): Beta for pruning.
            maximizingPlayer (bool): True if engine's turn.
            start_time (float): start time of the search for time control (optional).
            time_limit (float): time limit for the move (optional).

        Returns:
            (float, chess.Move): (score, best_move)
        """
        if start_time and time_limit and (time.time() - start_time >= time_limit):
            # Out of time, return evaluation immediately
            return self.evaluate_board(board), None

        if depth == 0 or board.is_game_over():
            self.nodes_searched += 1
            return self.evaluate_board(board), None

        board_key = (board.fen(), depth, maximizingPlayer)
        if board_key in self.transposition_table:
            # Use transposition table result if available and at least same depth
            stored = self.transposition_table[board_key]
            # You could use flag to decide exact or bound
            # For simplicity, assume exact storage
            return stored[0], stored[1]

        self.nodes_searched += 1

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return self.evaluate_board(board), None

        # Move ordering: sort moves by tactical potential (e.g., captures first, checks, etc.)
        legal_moves = self._order_moves(board, legal_moves)

        best_move = None
        if maximizingPlayer:
            max_eval = -math.inf
            for move in legal_moves:
                if start_time and time_limit and (time.time() - start_time >= time_limit):
                    break
                board.push(move)
                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, False, start_time, time_limit)
                board.pop()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = (max_eval, best_move)
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in legal_moves:
                if start_time and time_limit and (time.time() - start_time >= time_limit):
                    break
                board.push(move)
                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, True, start_time, time_limit)
                board.pop()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = (min_eval, best_move)
            return min_eval, best_move

    def _order_moves(self, board: chess.Board, moves):
        """
        Order moves to prioritize tactical and forcing moves:
        - Checks
        - Captures of high-value pieces
        - Other tactical motifs (fork, pin, skewer) - simplified as giving bonus to moves that are captures or checks.

        We can give a simple scoring:
        - +2 for delivering check
        - +1 * (value_of_captured_piece) for a capture
        """
        scored_moves = []
        for move in moves:
            score = 0
            # If move is a capture
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    score += self.piece_values.get(captured_piece.piece_type, 0)
            # If move gives check
            board.push(move)
            if board.is_check():
                score += 2
            board.pop()
            scored_moves.append((score, move))

        # Sort by score descending
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in scored_moves]

    def get_search_statistics(self):
        """
        Return the number of nodes searched in the last move and potentially other stats.
        """
        return {
            "nodes_searched": self.nodes_searched
        }
