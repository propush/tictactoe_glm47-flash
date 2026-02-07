#!/usr/bin/env python3
"""Entry point for Tic-Tac-Toe game."""

import sys
import threading

# Force colorama init for proper ANSI handling
try:
    from colorama import init
    init()
except ImportError:
    pass  # colorama not available, will use raw ANSI

# Import main game function
from tic_tac_toe.main import play_game


def main():
    """Main entry point for the game."""
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()