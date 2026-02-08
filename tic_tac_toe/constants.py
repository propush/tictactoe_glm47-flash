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
BOLD = "\033[1m"
DIM = "\033[2m"
REVERSE = "\033[7m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"

# UI Theme
TITLE = "TIC-TAC-TOE"
UI_WIDTH = 33
BORDER_CHAR = "="
GRID_H = "-"
GRID_V = "|"


# Board dimensions
BOARD_SIZE = 3

# Player markers
PLAYER = 'X'
COMPUTER = 'O'
