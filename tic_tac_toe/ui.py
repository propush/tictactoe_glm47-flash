"""Terminal UI functions for Tic-Tac-Toe game."""

import sys
from .constants import RESET, GREEN, RED, BOLD, PLAYER, COMPUTER


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


def display_result(player_won, is_draw):
    """Display game result.

    Args:
        player_won: True if player won
        is_draw: True if game ended in a draw
    """
    print("\n" + "=" * 30)
    if is_draw:
        print("It's a draw!")
    elif player_won:
        print("🎉 Congratulations! You win!")
    else:
        print("😔 Computer wins!")
    print("=" * 30 + "\n")


def display_scores(score_tracker):
    """Display current scores.

    Args:
        score_tracker: ScoreTracker instance
    """
    score_tracker.display_scores()


def display_play_again_prompt():
    """Display play again prompt and return user choice."""
    play_again = input("\nPlay again? (y/n): ").lower()
    if play_again != 'y':
        print("\nThanks for playing!")
    return play_again == 'y'