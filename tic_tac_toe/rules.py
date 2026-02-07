"""Game rules and logic for Tic-Tac-Toe.

Implements the Single Responsibility Principle by separating game logic
from game state management and display concerns.
"""

from .constants import BOARD_SIZE


class TicTacToeRules:
    """Rules and logic for Tic-Tac-Toe game."""

    @staticmethod
    def check_winner(board, player):
        """Check if the given player has won.

        Args:
            board: Current board state
            player: Player marker ('X' or 'O')

        Returns:
            True if player has won
        """
        # Check rows
        for i in range(BOARD_SIZE):
            if all(board[i][j] == player for j in range(BOARD_SIZE)):
                return True

        # Check columns
        for j in range(BOARD_SIZE):
            if all(board[i][j] == player for i in range(BOARD_SIZE)):
                return True

        # Check diagonals
        if all(board[i][i] == player for i in range(BOARD_SIZE)):
            return True
        if all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
            return True

        return False

    @staticmethod
    def is_full(board):
        """Check if the board is full.

        Args:
            board: Current board state

        Returns:
            True if board is full
        """
        return all(board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

    @staticmethod
    def make_move(board, row, col, player):
        """Place a piece on the board.

        Args:
            board: Current board state (modified in place)
            row: Row position (0-2)
            col: Column position (0-2)
            player: Player marker ('X' or 'O')

        Returns:
            True if move was successful, False otherwise
        """
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if board[row][col] == ' ':
                board[row][col] = player
                return True
        return False

    @staticmethod
    def get_available_moves(board):
        """Get all empty cells on the board.

        Args:
            board: Current board state

        Returns:
            List of (row, col) tuples for empty cells
        """
        return [(i, j) for i in range(BOARD_SIZE)
                for j in range(BOARD_SIZE) if board[i][j] == ' ']

    @staticmethod
    def check_game_over(board, player_won, computer_won):
        """Check if the game has ended.

        Args:
            board: Current board state
            player_won: True if player has won
            computer_won: True if computer has won

        Returns:
            Result dictionary with game state information
        """
        if player_won:
            return {'game_over': True, 'winner': 'player', 'reason': 'win'}
        if computer_won:
            return {'game_over': True, 'winner': 'computer', 'reason': 'win'}
        if TicTacToeRules.is_full(board):
            return {'game_over': True, 'winner': None, 'reason': 'draw'}
        return {'game_over': False}