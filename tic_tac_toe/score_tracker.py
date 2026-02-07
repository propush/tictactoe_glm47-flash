"""Score management and persistence for Tic-Tac-Toe game."""

import sys
import json
import os
from .constants import SCORE_FILE


class ScoreTracker:
    """Track game scores across multiple sessions with persistent storage."""

    def __init__(self, score_file=None):
        """Initialize score tracker and load scores from file if available.

        Args:
            score_file: Optional path to score file. Defaults to 'tic_tac_toe_scores.json'
        """
        self.score_file = score_file or SCORE_FILE
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.total_games = 0
        self.load_scores()

    def load_scores(self):
        """Load scores from file if it exists."""
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    self.player_wins = data.get('player_wins', 0)
                    self.computer_wins = data.get('computer_wins', 0)
                    self.draws = data.get('draws', 0)
                    self.total_games = data.get('total_games', 0)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or unreadable, start fresh
                self.player_wins = 0
                self.computer_wins = 0
                self.draws = 0
                self.total_games = 0

    def save_scores(self):
        """Save current scores to file."""
        try:
            data = {
                'player_wins': self.player_wins,
                'computer_wins': self.computer_wins,
                'draws': self.draws,
                'total_games': self.total_games
            }
            with open(self.score_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Warning: Could not save scores to file: {e}")

    def record_win(self, player_won, is_draw):
        """Record a win/loss/draw result.

        Args:
            player_won: True if player won
            is_draw: True if game ended in a draw
        """
        self.total_games += 1
        if player_won:
            self.player_wins += 1
        elif is_draw:
            self.draws += 1
        else:
            self.computer_wins += 1
        self.save_scores()  # Auto-save after recording

    def display_scores(self):
        """Display current session statistics."""
        sys.stdout.write("\n" + "=" * 30 + "\n")
        sys.stdout.write("📊 SESSION STATISTICS\n")
        sys.stdout.write("=" * 30 + "\n")
        sys.stdout.write(f"Player wins:      {self.player_wins}\n")
        sys.stdout.write(f"Computer wins:    {self.computer_wins}\n")
        sys.stdout.write(f"Draws:            {self.draws}\n")
        sys.stdout.write(f"Total games:      {self.total_games}\n")
        sys.stdout.write("=" * 30 + "\n")
        sys.stdout.flush()