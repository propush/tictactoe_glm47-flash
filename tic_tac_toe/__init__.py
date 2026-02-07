"""Tic-Tac-Toe game package.

This module provides a clean, modular Tic-Tac-Toe implementation
following Python design principles (KISS, Single Responsibility, etc.).
"""

from .game_coordinator import play_game, TicTacToeGame
from .game_state import GameState
from .rules import TicTacToeRules
from .ai_strategy import AIStrategyFactory
from .score_tracker import ScoreTracker

__all__ = [
    'play_game',
    'TicTacToeGame',
    'GameState',
    'TicTacToeRules',
    'AIStrategyFactory',
    'ScoreTracker',
]