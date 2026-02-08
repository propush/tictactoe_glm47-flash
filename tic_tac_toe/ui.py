"""Terminal UI functions for Tic-Tac-Toe game."""

import sys
from .constants import (
    RESET,
    GREEN,
    RED,
    YELLOW,
    BOLD,
    DIM,
    PLAYER,
    COMPUTER,
    Difficulty,
    GameResult,
    TITLE,
    UI_WIDTH,
    BORDER_CHAR,
)


def style(text, color=None, bold=False, dim=False):
    """Apply ANSI styles to text."""
    parts = []
    if bold:
        parts.append(BOLD)
    if dim:
        parts.append(DIM)
    if color:
        parts.append(color)
    parts.append(text)
    parts.append(RESET)
    return "".join(parts)


def print_header(title=TITLE):
    """Print a consistent header block."""
    rule = BORDER_CHAR * UI_WIDTH
    sys.stdout.write("\n" + rule + "\n")
    sys.stdout.write(f"{title:^{UI_WIDTH}}\n")
    sys.stdout.write(rule + "\n")


def print_footer():
    """Print a consistent footer rule."""
    sys.stdout.write(BORDER_CHAR * UI_WIDTH + "\n\n")


def display_menu():
    """Display game menu and instructions."""
    print_header()
    sys.stdout.write(
        f"\nYou are {style(PLAYER, bold=True)}, Computer is {style(COMPUTER, bold=True)}\n"
    )
    sys.stdout.write("\nNumber positions:\n")
    sys.stdout.write(" 1 2 3\n 4 5 6\n 7 8 9\n")
    sys.stdout.write("\nControls:\n")
    sys.stdout.write("  Arrow keys: Navigate cursor\n")
    sys.stdout.write(f"  Enter: Place your {style(PLAYER, bold=True)}\n")
    sys.stdout.write("  Ctrl+C: Cancel move or quit game\n")
    sys.stdout.write("  'q': Quit move selection mode\n")
    print_footer()


def display_instructions():
    """Display control instructions."""
    print_header()
    sys.stdout.write("\nControls:\n")
    sys.stdout.write("  Arrow keys: Navigate cursor\n")
    sys.stdout.write(f"  Enter: Place your {style(PLAYER, bold=True)}\n")
    sys.stdout.write("  Ctrl+C: Cancel move or quit game\n")
    sys.stdout.write("  'q': Quit move selection mode\n")
    print_footer()


def display_result(result):
    """Display game result.

    Args:
        result: GameResult value (PLAYER_WIN, COMPUTER_WIN, or DRAW)
    """
    print_header("GAME RESULT")
    if result == GameResult.DRAW:
        sys.stdout.write(style("It's a draw!", YELLOW, bold=True) + "\n")
    elif result == GameResult.PLAYER_WIN:
        sys.stdout.write(style("You win!", GREEN, bold=True) + "\n")
    else:
        sys.stdout.write(style("Computer wins!", RED, bold=True) + "\n")
    print_footer()


def display_scores(score_tracker):
    """Display current session statistics.

    Args:
        score_tracker: ScoreTracker instance
    """
    print_header("SESSION STATISTICS")
    sys.stdout.write(f"{'Player wins:':<16} {score_tracker.player_wins}\n")
    sys.stdout.write(f"{'Computer wins:':<16} {score_tracker.computer_wins}\n")
    sys.stdout.write(f"{'Draws:':<16} {score_tracker.draws}\n")
    sys.stdout.write(f"{'Total games:':<16} {score_tracker.total_games}\n")
    print_footer()
    sys.stdout.flush()


def get_difficulty_input():
    """Get difficulty level from user input.

    Returns:
        Difficulty constant (Difficulty.EASY, MEDIUM, or HARD)
    """
    choices = {
        '1': Difficulty.EASY,
        '2': Difficulty.MEDIUM,
        '3': Difficulty.HARD,
    }
    while True:
        choice = input(
            "\nSelect difficulty:\n"
            "1 - Easy (random moves)\n"
            "2 - Medium (basic strategy)\n"
            "3 - Hard (perfect play)\n"
            "Enter your choice (1-3): "
        ).strip()
        if choice in choices:
            return choices[choice]
        sys.stdout.write(style("Invalid choice. Please enter 1, 2, or 3.", RED) + "\n")


def display_play_again_prompt():
    """Display play again prompt and return user choice."""
    play_again = input("\nPlay again? (y/n): ").lower()
    if play_again != 'y':
        sys.stdout.write(style("\nThanks for playing!", DIM) + "\n")
    return play_again == 'y'
