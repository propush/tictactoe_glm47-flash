"""AI strategy pattern for Tic-Tac-Toe game.

Uses composition to combine different AI strategies.
"""

import copy
from abc import ABC, abstractmethod
from .constants import BOARD_SIZE, PLAYER, COMPUTER, Difficulty
from .rules import TicTacToeRules
from .board import get_random_move


class AIStrategy(ABC):
    """Abstract base class for AI strategies."""

    @abstractmethod
    def get_move(self, board):
        """Get the next move from the board.

        Args:
            board: Current board state (not modified)

        Returns:
            Tuple of (row, col) for the move, or None if no moves available
        """


class RandomMoveStrategy(AIStrategy):
    """Easy AI: Makes completely random valid moves."""

    def get_move(self, board):
        return get_random_move(board)


class MediumStrategy(AIStrategy):
    """Medium AI: Basic strategy (win/block/center/corner/side)."""

    def get_move(self, board):
        def is_winning_move(row, col, marker):
            test_board = copy.deepcopy(board)
            test_board[row][col] = marker
            return TicTacToeRules.check_winner(test_board, marker)

        # Try to win
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    if is_winning_move(i, j, COMPUTER):
                        return (i, j)

        # Try to block player
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    if is_winning_move(i, j, PLAYER):
                        return (i, j)

        # Take center if available
        if board[1][1] == ' ':
            return (1, 1)

        # Take a random corner
        corners = [(0, 0), (0, BOARD_SIZE - 1),
                   (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
        for i, j in corners:
            if board[i][j] == ' ':
                return (i, j)

        # Take a random side
        sides = [(0, 1), (1, 0), (1, BOARD_SIZE - 1),
                 (BOARD_SIZE - 1, 1)]
        for i, j in sides:
            if board[i][j] == ' ':
                return (i, j)

        return get_random_move(board)


class HardStrategy(AIStrategy):
    """Hard AI: Minimax algorithm for perfect play."""

    def get_move(self, board):
        work_board = copy.deepcopy(board)

        def minimax(board_state, maximizing_player, alpha, beta):
            """Minimax algorithm with alpha-beta pruning."""
            if TicTacToeRules.check_winner(board_state, COMPUTER):
                return 1
            if TicTacToeRules.check_winner(board_state, PLAYER):
                return -1
            if TicTacToeRules.is_full(board_state):
                return 0

            if maximizing_player:
                max_score = -float('inf')
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        if board_state[i][j] == ' ':
                            board_state[i][j] = COMPUTER
                            score = minimax(board_state, False, alpha, beta)
                            board_state[i][j] = ' '
                            max_score = max(max_score, score)
                            alpha = max(alpha, max_score)
                            if alpha >= beta:
                                return max_score
                return max_score
            else:
                min_score = float('inf')
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        if board_state[i][j] == ' ':
                            board_state[i][j] = PLAYER
                            score = minimax(board_state, True, alpha, beta)
                            board_state[i][j] = ' '
                            min_score = min(min_score, score)
                            beta = min(beta, min_score)
                            if beta <= alpha:
                                return min_score
                return min_score

        best_score = -float('inf')
        best_move = None

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if work_board[i][j] == ' ':
                    work_board[i][j] = COMPUTER
                    score = minimax(work_board, False, -float('inf'), float('inf'))
                    work_board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move


class AIStrategyFactory:
    """Factory for creating AI strategy instances."""

    _strategies = {
        Difficulty.EASY: RandomMoveStrategy,
        Difficulty.MEDIUM: MediumStrategy,
        Difficulty.HARD: HardStrategy,
    }

    @classmethod
    def create(cls, difficulty):
        """Create strategy instance from difficulty.

        Args:
            difficulty: Difficulty level (Difficulty.EASY, MEDIUM, or HARD)

        Returns:
            AIStrategy instance
        """
        strategy_class = cls._strategies.get(difficulty, RandomMoveStrategy)
        return strategy_class()
