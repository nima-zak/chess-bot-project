import chess
import math


class Engine:
    def __init__(self, color_is_white=True):
        """
        The Engine class handles the chess AI logic, including board evaluation,
        decision-making via Minimax with Alpha-Beta pruning, and move selection.

        Args:
            color_is_white (bool): True if the engine plays as White, False if Black.
        """
        self.color_is_white = color_is_white

        # Basic piece values
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.25,  # Slightly higher than knight
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        # Central squares considered important for positional control
        self.center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]

    def evaluate_board(self, board: chess.Board):
        """
        Evaluate the board position from the engine's perspective.

        This evaluation considers:
        - Material balance
        - Pawn structure (isolated, doubled, advanced pawns)
        - King safety (number of safe squares, protection)
        - Control of the center
        - Potentially other positional factors

        Returns:
            float: A score representing the advantage (positive) or disadvantage (negative).
        """
        if board.is_game_over():
            # Check endgame conditions
            if board.is_checkmate():
                # If checkmate: the side to move lost.
                # If engine is to move and it's checkmate, engine lost => large negative.
                # Otherwise engine won => large positive.
                if board.turn == self.color_is_white:
                    return -9999
                else:
                    return 9999
            else:
                # Draw or stalemate
                return 0

        # Calculate various scores
        material_score = self._material_score(board)
        pawn_score = self._pawn_structure_score(board)
        king_score = self._king_safety_score(board)
        center_score = self._center_control_score(board) + self._active_piece_bonus(board)

        total_score = material_score + pawn_score + king_score + center_score

        # If engine is black, invert the sign because we evaluated from white's perspective
        if not self.color_is_white:
            total_score = -total_score

        return total_score

    def _material_score(self, board: chess.Board):
        """
        Compute material balance: sum of white pieces value minus black pieces value.
        """
        score = 0.0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                val = self.piece_values[piece.piece_type]
                if piece.color:  # White piece
                    score += val
                else:
                    score -= val
        return score

    def _pawn_structure_score(self, board: chess.Board):
        """
        Evaluate pawn structure:
        - Isolated pawns: no friendly pawn on adjacent files => penalty
        - Doubled pawns: multiple pawns on the same file => penalty
        - Advanced pawns: pawns close to promotion rank might get a small bonus.
        """
        score = 0.0

        white_pawns = [sq for sq in chess.SQUARES if board.piece_at(sq)
                       and board.piece_at(sq).piece_type == chess.PAWN
                       and board.piece_at(sq).color]
        black_pawns = [sq for sq in chess.SQUARES if board.piece_at(sq)
                       and board.piece_at(sq).piece_type == chess.PAWN
                       and not board.piece_at(sq).color]

        # Check doubled pawns
        white_files = [chess.square_file(p) for p in white_pawns]
        black_files = [chess.square_file(p) for p in black_pawns]

        for f in range(8):
            w_count = white_files.count(f)
            if w_count > 1:
                score -= 0.1 * (w_count - 1)  # penalty for white doubled pawns
            b_count = black_files.count(f)
            if b_count > 1:
                score += 0.1 * (b_count - 1)  # black doubled pawns bad for black, good for white

        # Isolated pawns
        def isolated_pawns(pawn_squares, pawn_files, white_side):
            iso_score = 0.0
            for i, sq in enumerate(pawn_squares):
                pf = pawn_files[i]
                left_file_pawns = (pf - 1 in pawn_files)
                right_file_pawns = (pf + 1 in pawn_files)
                if not left_file_pawns and not right_file_pawns:
                    # isolated pawn
                    if white_side:
                        iso_score -= 0.15
                    else:
                        iso_score += 0.15
            return iso_score

        score += isolated_pawns(white_pawns, white_files, True)
        score += isolated_pawns(black_pawns, black_files, False)

        # Advanced pawns (closer to promotion)
        # For white, higher rank = more advanced
        # For black, lower rank = more advanced
        for wp in white_pawns:
            rank = chess.square_rank(wp)
            # White pawns start at rank 1, so rank closer to 7 => more advanced
            # Give small bonus for each rank advanced
            score += (rank - 1) * 0.02
        for bp in black_pawns:
            rank = chess.square_rank(bp)
            # Black pawns start at rank 6 (0-based rank=6?), actually black starts at rank 6 (0-based index)
            # The closer to rank 0, the more advanced.
            # rank 6 => start, rank 0 => promotion line
            score += (6 - rank) * 0.02

        return score

    def _king_safety_score(self, board: chess.Board):
        """
        Evaluate king safety by checking:
        - Safe squares around the king.
        - Friendly pieces protecting the king.

        This is a very simplified heuristic.
        """
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
                # If empty or same color piece, consider it safe (very simplistic)
                if piece is None or piece.color == color:
                    safe_squares += 1

            # Count friendly pieces near king
            friendly_count = 0
            for m in moves:
                p = board.piece_at(m)
                if p and p.color == color and p.piece_type != chess.KING:
                    friendly_count += 1

            # More safe squares and more friendly pieces => better safety
            return (safe_squares * 0.05) + (friendly_count * 0.1)

        score += king_safety(white_king, True)
        score -= king_safety(black_king, False)

        return score

    def _center_control_score(self, board: chess.Board):
        """
        Gives a small bonus for controlling center squares.
        Already implemented before, we keep it here.
        """
        score = 0.0
        for sq in self.center_squares:
            piece = board.piece_at(sq)
            if piece:
                if piece.color:  # white
                    score += 0.1
                else:
                    score -= 0.1
        return score

    def _active_piece_bonus(self, board: chess.Board):
        """
        Give a small bonus for pieces that are out and active (not stuck behind pawns, etc.).
        A simplified approach: count how many pieces (except pawns) are placed
        beyond their initial two ranks, giving them a slight bonus if white,
        and a penalty if black is too advanced (from white's perspective).

        This is very simplistic and optional.
        """
        score = 0.0
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece and piece.piece_type != chess.PAWN and piece.piece_type != chess.KING:
                rank = chess.square_rank(sq)
                if piece.color:  # white
                    # White pieces beyond rank 1 (0-based) get small bonus
                    if rank > 1:
                        score += 0.05
                else:
                    # Black pieces beyond rank 6 (0-based) means they advanced into white's territory
                    if rank < 6:
                        score -= 0.05
        return score

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizingPlayer: bool):
        """
        Minimax with Alpha-Beta pruning.

        Args:
            board (chess.Board): current position
            depth (int): search depth
            alpha (float): alpha value for pruning
            beta (float): beta value for pruning
            maximizingPlayer (bool): True if engine's turn, else minimizing.

        Returns:
            (float, chess.Move): (evaluation, best_move)
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return self.evaluate_board(board), None

        best_move = None

        if maximizingPlayer:
            max_eval = -math.inf
            for move in legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def find_best_move(self, board: chess.Board, depth: int):
        """
        Find the best move from the current position using Minimax and Alpha-Beta pruning.

        Args:
            board (chess.Board): current board state
            depth (int): search depth

        Returns:
            chess.Move: the best move found
        """
        current_turn_is_white = board.turn
        maximizingPlayer = (self.color_is_white == current_turn_is_white)
        _, best_move = self.minimax(board, depth, -math.inf, math.inf, maximizingPlayer)
        return best_move
