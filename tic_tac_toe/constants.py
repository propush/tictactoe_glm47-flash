"""Constants and configuration for Tic-Tac-Toe game."""

# Save file for persistent scores
SCORE_FILE = "tic_tac_toe_scores.json"


class Difficulty:
    """AI difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameResult:
    """Possible game outcomes."""
    PLAYER_WIN = "player_win"
    COMPUTER_WIN = "computer_win"
    DRAW = "draw"


# ANSI Color Codes
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
BOLD = "\033[1m"


# Board dimensions
BOARD_SIZE = 3

# Player markers
PLAYER = 'X'
COMPUTER = 'O'