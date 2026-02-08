"""Terminal UI functions for Tic-Tac-Toe game."""

import sys
from .constants import RESET, GREEN, RED, BOLD, PLAYER, COMPUTER, Difficulty, GameResult


def display_menu():
    """Display game menu and instructions."""
    print("\n" + "=" * 30)
    print("🎮 TIC-TAC-TOE")
    print("=" * 30)
    print("\nYou are " + BOLD + PLAYER + RESET + ", Computer is " + BOLD + COMPUTER + RESET)
    print("\nNumber positions:")
    print(" 1 2 3")
    print(" 4 5 6")
    print(" 7 8 9")
    print("\nControls:")
    print("  Arrow keys: Navigate cursor")
    print("  Enter: Place your " + BOLD + PLAYER + RESET)
    print("  Ctrl+C: Cancel move or quit game")
    print("  'q': Quit move selection mode")
    print("=" * 30 + "\n")


def display_instructions():
    """Display control instructions."""
    print("\n" + "=" * 30)
    print("🎮 TIC-TAC-TOE")
    print("=" * 30)
    print("\nControls:")
    print("  Arrow keys: Navigate cursor")
    print("  Enter: Place your X")
    print("  Ctrl+C: Cancel move or quit game")
    print("  'q': Quit move selection mode")
    print("=" * 30 + "\n")


def display_result(result):
    """Display game result.

    Args:
        result: GameResult value (PLAYER_WIN, COMPUTER_WIN, or DRAW)
    """
    print("\n" + "=" * 30)
    if result == GameResult.DRAW:
        print("It's a draw!")
    elif result == GameResult.PLAYER_WIN:
        print("🎉 Congratulations! You win!")
    else:
        print("😔 Computer wins!")
    print("=" * 30 + "\n")


def display_scores(score_tracker):
    """Display current session statistics.

    Args:
        score_tracker: ScoreTracker instance
    """
    sys.stdout.write("\n" + "=" * 30 + "\n")
    sys.stdout.write("📊 SESSION STATISTICS\n")
    sys.stdout.write("=" * 30 + "\n")
    sys.stdout.write(f"Player wins:      {score_tracker.player_wins}\n")
    sys.stdout.write(f"Computer wins:    {score_tracker.computer_wins}\n")
    sys.stdout.write(f"Draws:            {score_tracker.draws}\n")
    sys.stdout.write(f"Total games:      {score_tracker.total_games}\n")
    sys.stdout.write("=" * 30 + "\n")
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
        choice = input("\nSelect difficulty:\n"
                       "1 - Easy (random moves)\n"
                       "2 - Medium (basic strategy)\n"
                       "3 - Hard (perfect play)\n"
                       "Enter your choice (1-3): ").strip()
        if choice in choices:
            return choices[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def display_play_again_prompt():
    """Display play again prompt and return user choice."""
    play_again = input("\nPlay again? (y/n): ").lower()
    if play_again != 'y':
        print("\nThanks for playing!")
    return play_again == 'y'
