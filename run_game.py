#!/usr/bin/env python3
"""Standalone script to run Tic-Tac-Toe game."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tic_tac_toe.game_coordinator import play_game


def main():
    """Main entry point."""
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()