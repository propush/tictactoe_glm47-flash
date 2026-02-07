"""Main game loop and coordination for Tic-Tac-Toe game.

This module is deprecated. Please use the new game_coordinator module.
Keeping for backward compatibility.
"""

import sys
from .game_coordinator import play_game as play_game_new


def play_game():
    """Main game loop. Uses new architecture."""
    play_game_new()