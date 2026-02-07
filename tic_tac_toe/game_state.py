"""Game state management for Tic-Tac-Toe.

Implements the Single Responsibility Principle by managing game state
separately from game rules and display concerns.
"""

from .constants import BOARD_SIZE, PLAYER, COMPUTER


class GameState:
    """Manages the current state of a Tic-Tac-Toe game."""

    def __init__(self):
        """Initialize a new game state."""
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER
        self.is_active = True
        self.game_over_reason = None

    def reset(self):
        """Reset the game to initial state."""
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER
        self.is_active = True
        self.game_over_reason = None

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = COMPUTER if self.current_player == PLAYER else PLAYER

    def get_player_marker(self):
        """Get the current player's marker.

        Returns:
            Current player marker ('X' or 'O')
        """
        return self.current_player

    def is_player_turn(self):
        """Check if it's the player's turn.

        Returns:
            True if it's player's turn, False otherwise
        """
        return self.current_player == PLAYER